import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() path: any;
    public images: any;
    public code = 200;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loading(true);
        await this.load();
        await this.loading(false);
    }

    public async load() {
        let { code, data } = await wiz.call("load", { path: this.path });
        this.code = code;
        if (code != 200) {
            return
        }
        this.images = data;
        await this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}