import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() title: any;

    private list = [];

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        const { code, data } = await wiz.call("load");
        if (code !== 200) {
            let msg = "인기 검색어를 불러오는 과정에서 오류가 발생했습니다.";
            await this.alert(msg);
            return;
        }
        this.list = data;
    }

    private async alert(message: string, status: string = 'error') {
        return await this.service.alert.show({
            title: "",
            message: message,
            cancel: false,
            actionBtn: status,
            action: "확인",
            status: status
        });
    }

    private async search(text) {
        const { code } = await wiz.call("log", { text });
        if (code !== 200) {
            let msg = "검색 과정에서 오류 발생!";
            await this.alert(msg);
            return;
        }
        
        let url = "/dataset/search?text=" + text;
        this.service.href(url);
    }
}