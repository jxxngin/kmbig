import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';

export class Component implements OnInit {

    public category = {
        "device": "기기",
        "blood": "혈자리",
        "herbal_medicine": "한약재",
        "medical_institution": "의료기관",
        "decoction": "탕약"
    };

    public category_ls = {
        id: "",
        title: "",
        category: "",
        content: ""
    }
    public dataset_ls = []

    public dataset_id: any;

    public labels = ['CHART 1', 'CHART 2', 'CHART 3', 'CHART 4'];
    public datas = [80, 40, 50, 50];
    public colors = ['#5041F2', '#F2748D', '#9996B7', '#DFDEF7']

    constructor(
        public service: Service,
        public router: Router
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();

        this.dataset_ls[0].css_class = "menu-card2";

        await this.service.render();
    }

    public async load() {
        this.dataset_id = this.router.url.split('/')[2];
        let { code, data } = await wiz.call("load", { "id": this.category[this.dataset_id] });
        this.dataset_ls = data.dataset_row;
        this.category_ls = data.dashboard_row;
        await this.service.render();
    }

    public click(url) {
        this.service.href([`/dashboard/device/${url}`]);
    }

    public click2(url) {
        for (let i = 0; i < this.dataset_ls.length; i++) {
            if (url == this.dataset_ls[i].id) {
                this.dataset_ls[i].css_class = "menu-card2";
                this.link = url;
            }
            else this.dataset_ls[i].css_class = "menu-card";
        }
        this.service.render();
    }
}