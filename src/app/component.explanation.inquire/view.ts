import { OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Output() filterResult = new EventEmitter<object>();
    @Output() offcanvas = new EventEmitter<boolean>();

    public period = [2020, 2021, 2022];
    public sex = ["여자", "남자"];
    // public age = ["0~9세", "10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대", "90대", "100세 이상"];
    public age1 = ["0~9세", "10대", "20대", "30대", "40대", "50대"];
    public age2 = ["60대", "70대", "80대", "90대", "100세 이상"];
    public sasang = ["태양인", "태음인", "소양인", "소음인"];
    public weight1: any;
    public weight2: any;
    public height1: any;
    public height2: any;
    public ages: any;

    public test = false;
    public num: any;

    public filter = {
        period: {},
        age: {},
        sex: {},
        sasang: {},
        height1: "",
        height2: "",
        weight1: "",
        weight2: "",
    };

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.dataID = WizRoute.segment.id;
        await this.service.render();
    }

    public async result() {
        await this.loading(true);
        let copyFilter = JSON.stringify(this.filter);
        let { code, data } = await wiz.call("result", { id: this.dataID, filter: copyFilter });
        if (code != 200) return;
        this.num = data;
        this.test = true;
        await this.service.render();
        await this.loading(false);
    }

    public async push() {
        this.filterResult.emit(this.filter);
        this.offcanvas.emit(true);
        await this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}