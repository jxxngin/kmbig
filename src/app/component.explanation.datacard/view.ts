import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {

    constructor(
        public service: Service
    ) { }

    public category: any;
    public category_ls = {
        "device": "기기",
        "blood": "혈자리",
        "herbal_medicine": "한약재",
        "medical_institution": "의료기관",
        "decoction": "탕약"
    };

    public async ngOnInit() {
        await this.service.init();
        await this.load();
        await this.service.render();
    }

    public async load() {
        this.category = WizRoute.segment.category;
        let { code, data } = await wiz.call("load", { category: this.category_ls[this.category] });
        if (code != 200) return;
        this.list = data;
    }

    public async dataset(id) {
        // this.service.href(`/dashboard/${this.category}/${id}`);
        location.href = "/dashboard/" + this.category + "/" + id;
    }
}