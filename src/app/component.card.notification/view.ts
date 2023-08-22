import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private list = [];
    private isAnimating = false;

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.load();
    }

    private async load() {
        const { code, data } = await wiz.call("load");
        if (code !== 200) {
            alert("[ERROR] load list");
            return;
        }
        this.list = data;
        await this.service.render();
    }

    private async show(item) {
        if (item.show !== 1) {
            const { code } = await wiz.call("update", { id: item.id });
            if (code !== 200) {
                alert("[ERROR] update show");
                return;
            }
        }

        if (item.title == "전문가 심사 요청") {
            this.service.href("share/expert/form/view/" + item.id);
        }
        else if (item.title == "데이터셋 공유 요청") {
            this.service.href("/share/user/form/view/" + item.id);
        }
        await this.load();
    }

    private async refresh() {
        this.isAnimating = true;

        setTimeout(async () => {
            this.isAnimating = false;
        }, 400);

        await this.load();
    }
}