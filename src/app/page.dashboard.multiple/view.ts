import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';

export class Component implements OnInit {

    public category = {
        "device": "기기",
        "blood": "혈자리",
        "medicine": "한약재",
        "multiple": "응용"
    };

    public category_ls = {
        id: "",
        title: "",
        category: "",
        content: ""
    }
    public dataset_ls = []
    public dataset_id: any;

    constructor(
        public service: Service,
        public router: Router
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
        await this.service.render();
    }

    public async load() {
        this.dataset_id = this.router.url.split('/')[2];
        let { code, data } = await wiz.call("load", { "id": this.category[this.dataset_id] });
        this.dataset_ls = data.dataset_row;
        this.category_ls = data.dashboard_row;
        await this.service.render();
    }
}