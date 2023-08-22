import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';

export class Component implements OnInit {
    // @Input() title: any;

    public dashboard_ls = [
        { url: "/dashboard/device", name: "기기 데이터셋", content: " (기기)" },
        { url: "/dashboard/blood", name: "혈자리 데이터셋", content: " (혈자리)" },
        { url: "/dashboard/herbal_medicine", name: "한약재 데이터셋", content: " (한약재)" },
        { url: "/dashboard/medical_institution", name: "의료기관 데이터셋", content: " (의료기관)" },
        { url: "/dashboard/decoction", name: "탕약 데이터셋", content: " (탕약)" }];

    public category = {
        "device": "기기",
        "blood": "혈자리",
        "herbal_medicine": "한약재",
        "medical_institution": "의료기관",
        "decoction": "탕약"
    };

    public category_ls = {
        id: "",
        category: "",
        content: ""
    }
    public dataset_ls = []

    public labels = ['CHART 1', 'CHART 2', 'CHART 3', 'CHART 4'];
    public datas = [80, 40, 50, 50];
    public colors = ['#5041F2', '#F2748D', '#9996B7', '#DFDEF7'];
    
    constructor(
        public service: Service,
        public router: Router
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();

        this.dataset_ls[0].css_class = "menu-card2";
        // this.link = this.dataset_ls[0].url;
        this.link = this.dataset_ls[0].id;
        this.currentRoute = this.router.url;
        for (let menu of this.dashboard_ls) {
            if (this.currentRoute == menu.url) {
                this.dataset_name = menu.name;
                this.dataset_content = menu.content;
                break
            }
        }

        this.router.events.subscribe((event: Event) => {
            if (event instanceof NavigationEnd) {
                this.currentRoute = event.url;

                for (let menu of this.dashboard_ls) {
                    if (this.currentRoute == menu.url) {
                        this.dataset_name = menu.name;
                        this.dataset_content = menu.content;
                        break
                    }
                }
                this.load();
            }
        })
        await this.service.render();
    }

    public async load() {
        this.dataset_id = WizRoute.segment.category;
        console.log('ddd : ', this.dataset_id)
        let { code, data } = await wiz.call("load", { "id": this.category[this.dataset_id] });
        console.log('code : ', code)
        this.dataset_ls = data.dataset_row;
        this.category_ls = data.dashboard_row;
        await this.service.render();
    }

    public click(url) {
        this.service.href(`/dashboard/device/${url}`);
    }

    public click2(url) {
        for (let i = 0; i < this.dataset_ls.length; i++) {
            // if (url == this.dataset_ls[i].url) {
            if (url == this.dataset_ls[i].id) {
                this.dataset_ls[i].css_class = "menu-card2";
                this.link = url;
            }
            else this.dataset_ls[i].css_class = "menu-card";
        }
        this.service.render();
    }
}