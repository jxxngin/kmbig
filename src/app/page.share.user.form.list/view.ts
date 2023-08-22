import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {

    private mode = "";
    public page = {
        start: 1,
        end: 1,
        current: 1,
    };

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.changeRank();
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

    private async changeRank() {
        const selectElement = document.querySelector('select') as HTMLSelectElement;

        if (selectElement) {
            const selectedValue = selectElement.value;
            this.mode = selectedValue;
            await this.load();
        }
    }

    public click(url) {
        this.service.href(`/share/user/form/view/${url}`);
    }

    private pageLoad(p: number) {
        this.page.current = p;
        this.load();
    }
}