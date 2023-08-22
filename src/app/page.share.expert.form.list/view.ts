import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {

    private mode = "default";
    public page = {
        start: 1,
        end: 1,
        current: 1,
    };

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        let init = await this.service.init();
        if (Object.keys(init.auth.session).length === 0 || init.auth.session.is_expert==0) {
            this.service.href(`/`);
            return;
        }
        await this.load();
        await this.pageLoad(1);
        await this.service.render();
    }

    public async load() {
        let { code, data } = await wiz.call("load", { mode: this.mode, page: this.page.current });
        this.list = data.rows;

        this.lastpage = data.lastpage;
        this.page.start = (parseInt((this.page.current - 1) / 10) * 10) + 1;
        this.page.end = this.lastpage;

        await this.service.render();
    }

    public click(url) {
        this.service.href(`/share/expert/form/view/${url}`);
    }

    private pageLoad(p: number) {
        this.page.current = p;
        this.load();
    }
}