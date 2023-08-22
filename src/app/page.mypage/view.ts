import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) { }

    public data: any = {};

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow(true, "/auth/login");
        await this.load();
    }

    public async alert(message: string, status: any = "error") {
        return await this.service.alert.show({
            title: '',
            message: message,
            cancel: false,
            actionBtn: status,
            action: "확인",
            status: status
        });
    }

    public async load() {
        const { data } = await wiz.call("session");

        this.data.user = data;
        this.data.password = {}

        await this.service.render();
    }

    public async update() {
        let userinfo = JSON.stringify(this.data.user);
        const { code, data } = await wiz.call("update", { userinfo });
        if (code == 200) {
            this.alert("저장되었습니다", 'success');
            await this.load();
            return;
        }

        await this.alert("오류가 발생했습니다");
    }

    public async changePassword() {
        let pdata = JSON.parse(JSON.stringify(this.data.password));

        if (!pdata.current) {
            await this.alert("현재 비밀번호를 입력해주세요");
            return;
        }
        if (!pdata.data || !pdata.repeat) {
            await this.alert("변경 비밀번호를 입력해주세요");
            return;
        }

        if (pdata.data != pdata.repeat) {
            await this.alert("변경 비밀번호를 다시 확인해주세요");
            return;
        }

        let pd = {};
        pd.current = this.service.auth.hash(pdata.current);
        pd.data = this.service.auth.hash(pdata.data);

        const { code, data } = await wiz.call("change_password", pd);

        if (code != 200) {
            await this.alert(data);
            return;
        }

        location.href = "/auth/logout";
    }

}