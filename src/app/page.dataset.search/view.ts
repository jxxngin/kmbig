import { OnInit } from '@angular/core';
import { Router, ActivatedRoute, Event, NavigationEnd } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public data = [];
    public category = {
        '기기': 'device',
        '혈자리': 'blood',
        '한약재': 'herbal_medicine',
        '의료기관': 'medical_institution',
        '탕약': 'decoction'
    };

    private total = 0;
    private mode = "default";
    public page = {
        start: 1,
        end: 1,
        current: 1,
    };

    public facet = {};
    public advfacet = {};

    public filter = {
        category: {},
        department: {},
        filetype: {},
        visibility: {},
    };

    private search = {
        text: "",
        checked: false,
    };

    private isAnimating = false;
    private _loading = false;

    constructor(
        public service: Service,
        private router: Router,
        private route: ActivatedRoute,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.search.text = decodeURIComponent(location.search).split("=")[1];
        await this.pageLoad(1);

        // this.route.params.subscribe(async (text) => {
        //     this.search.text = text;
        //     await this.pageLoad(1);
        // });
        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.search.text = decodeURIComponent(location.search).split("=")[1];
                await this.pageLoad(1);
            }
        })
        await this.service.render();
    }

    public async load() {
        await this.loading(true);

        if (this.search.text === undefined) {
            this.search.text = "";
        }

        let { code, data } = await wiz.call("load", {
            page: this.page.current,
            text: this.search.text,
            mode: this.mode,
            checked: JSON.stringify(this.filter),
        });
        if (code !== 200) {
            alert('ERROR!');
            return;
        }

        this.data = data.list;
        this.facet = data.facet;

        for (let i = 0; i < this.facet.department.length; i++) {
            if (this.facet.department[i].name === null && this.facet.department[i].cnt === 0) {
                this.facet.department.splice(i, 1);
            }
        }

        for (let category in this.facet) {
            this.advfacet[category] = {};

            for (let i = 0; i < this.facet[category].length; i++) {
                let obj = this.facet[category][i];
                this.advfacet[category][obj.name] = obj.cnt;
            }
        }

        for (let i = 0; i < this.data.length; i++) {
            this.data[i].tags = JSON.parse(this.data[i].tags);
            this.data[i].created = this.data[i].created.substring(0, 10);
            this.data[i].updated = this.data[i].updated.substring(0, 10);
        }

        this.total = data.total;
        this.lastpage = data.lastpage;
        this.page.start = (parseInt((this.page.current - 1) / 10) * 10) + 1;
        this.page.end = this.lastpage;

        await this.loading(false);
        await this.service.render();
    }

    private pageLoad(p: number) {
        this.page.current = p;
        this.load();
    }

    public click(item) {
        let category = this.category[item.category];
        this.service.href(`/dashboard/${category}/${item.id}`);
    }

    private async refresh() {
        this.isAnimating = true;

        setTimeout(async () => {
            this.isAnimating = false;
        }, 400);

        this.filter = {
            category: {},
            department: {},
            filetype: {},
            visibility: {},
        };
        await this.pageLoad(1);
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }

    public async move(id) {
        this.service.href(`/dashboard/device/${id}`);
    }
}