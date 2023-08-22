import { OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public dataset: string = "기기 데이터셋";
    // public list = ['기기 데이터셋', '혈자리 데이터셋', '한약재 데이터셋', '의료기관 데이터셋', '탕약 데이터셋'];
    public list = ['기기 데이터셋', '혈자리 데이터셋', '한약재 데이터셋', '의료기관 데이터셋'];
    private device = [];

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.load();
        await this.service.render();
    }

    private async load() {
        const { code, data } = await wiz.call("load");
        this.device = data;
    }

    private async change(mode) {
        this.dataset = mode;
        await this.service.render();
    }

    private async onClick(idx) {
        let url = this.device[idx].url;
        await this.service.href(url);
    }
}