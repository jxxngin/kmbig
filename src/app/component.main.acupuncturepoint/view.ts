import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private acupuncture_point: string = "수태음폐경(LU)";
    private images = {};
    private col1 = [];
    private col2 = [];

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.load();
        this.setPath();
    }

    private async load() {
        let { code, data } = await wiz.call('load');

        const { col1, col2 } = data;
        this.col1 = col1;
        this.col2 = col2;

        await this.service.render();
    }

    private async change(point) {
        this.acupuncture_point = point;
        this.setPath();
    }

    private async setPath() {
        let { code, data } = await wiz.call("path", { point: this.acupuncture_point });
        this.images = data;
        await this.service.render();
    }
}