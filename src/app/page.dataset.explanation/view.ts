import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    public dashboard_ls = [
        { url: "/dashboard/device", name: "기기 데이터셋", content: " (기기)" },
        { url: "/dashboard/blood", name: "혈자리 데이터셋", content: " (혈자리)" },
        { url: "/dashboard/herbal_medicine", name: "한약재 데이터셋", content: " (한약재)" },
        { url: "/dashboard/medical_institution", name: "의료기관 데이터셋", content: " (의료기관)" },
        { url: "/dashboard/decoction", name: "탕약 데이터셋", content: " (탕약)" }];

    public list = [];
    public down = false;
    public columns: any;

    public mode: any;
    public status: any;
    public statusContent: any;
    public shareInfo = [];
    // public shareInfo = {
    //     content: "",
    //     dataset_name: "",
    //     purpose: "",
    //     status: "",
    //     status_class: "",
    //     status_name: ""
    // };
    public purpose: any;
    public content: any;

    public use = true;

    public period = [2020, 2021, 2022];
    public sex = ["여자", "남자"];
    public age = ["0~9세", "10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대", "90대", "100세 이상"];
    public sasang = ["태양인", "태음인", "소양인", "소음인"];
    public weight1: any;
    public weight2: any;
    public height1: any;
    public height2: any;
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

    private tab = "share";
    private listMode = "list";
    private history = [];

    constructor(
        public service: Service,
        public router: Router
    ) { }

    public async ngOnInit() {
        let init = await this.service.init();
        if (Object.keys(init.auth.session).length === 0) this.use = false;

        this.mode = 'preview';
        this.dataset_id = WizRoute.segment.id;
        this.category = WizRoute.segment.category;
        this.userID = this.service.auth.session.id;
        await this.load();
        console.log("filter : ", this.filter)

        this.currentRoute = this.router.url;
        for (let menu of this.dashboard_ls) {
            if (this.currentRoute.indexOf(menu.url) == 0) {
                this.dashboard_name = menu.name;
                this.dashboard_url = menu.url;
                break
            }
        }

        await this.service.render();

        this.router.events.subscribe((event: Event) => {
            if (event instanceof NavigationEnd) {
                this.currentRoute = event.url;

                for (let menu of this.dashboard_ls) {
                    if (this.currentRoute.indexOf(menu.url) == 0) {
                        this.dataset_name = menu.name;
                        this.dataset_content = menu.content;
                        break
                    }
                }
                this.service.render();
            }
        })

        await this.service.render();
    }

    public async alert(message: string, status: string = 'error', cancel: any = false, action: string = '확인') {
        return await this.service.alert.show({
            title: "",
            message: message,
            cancel: cancel,
            actionBtn: status,
            action: action,
            status: status
        });
    }

    public async load() {
        let { code, data } = await wiz.call("info", { "category": this.category, "id": this.dataset_id });
        this.list = data;
        this.list.tags = JSON.parse(this.list.tags);
        this.list.period = JSON.parse(this.list.period);
        this.list.schema = JSON.parse(this.list.schema);
        this.list.created = this.list.created.substr(0, 10);
        this.list.updated = this.list.updated.substr(0, 10);
        if (!this.shareInfo) {
            this.status = "nothing";
        }
        await this.getInfo();
        await this.service.render();
    }

    private async getInfo() {
        let { code, data } = await wiz.call("shareInfo", { "id": this.dataset_id });
        this.shareInfo = data;
        console.log("info : ", this.shareInfo)
        if (code == 200) {
            for (let i = 0; i < this.shareInfo.length; i++) {
                if (this.shareInfo[i].filter) {
                    this.shareInfo[i].filter = JSON.parse(this.shareInfo[i].filter.replace(/'/g, '"').replace(/True/g, 'true').replace(/False/g, 'false'));
                }
                this.shareInfo[i].tag = await this.showFilter(this.shareInfo[i].filter);
            }
        }
    }

    public async share() {
        this.down = true;
        await this.service.render();
    }

    // 데이터 건수 조회
    public async shareFilter(e) {
        this.filter = e;
        await this.service.render();
    }
    public async offBool(o) {
        this.down = o;
        await this.service.render();
    }

    public close() {
        this.down = false;
        this.service.render();
    }

    public async request() {
        if (!this.purpose) {
            await this.alert("활용 목적을 선택해주세요.", "error")
        } else if (!this.content) {
            await this.alert("데이터셋 공유 요청 목적을 작성해주세요.", "error");
        } else {
            let res = await this.alert(this.list.title + " 데이터셋 공유 요청하시겠습니까?", "success", "취소");
            if (res) {
                await this.loading(true);
                let copyFilter = JSON.stringify(this.filter)
                let { code, data } = await wiz.call("request", { "userID": this.userID, "purpose": this.purpose, "content": this.content, "id": this.dataset_id, "name": this.list.title, "filter": copyFilter });
                if (code == 200) {
                    await this.loading(false);
                    await this.alert("공유 심사 결과 확인은 해당 페이지 혹은 데이터셋 공유 -> 내 공유요청 목록 페이지에서 확인해주세요.", "success")
                    await this.service.href(`/share/user/form/view/${data}`);
                }
            }
        }
    }

    public async download() {
        console.log("docID : ", this.shareInfo.id)
        let download = wiz.url('download?id=' + this.dataset_id + "&title=" + this.list.title + "&docID=" + this.history.id)
        // window.open(download, '_blank');
        window.location.href = download;
    }

    public async drive() {
        let res = await this.alert(this.list.title + " 데이터셋을 연구자 서랍에 저장하시겠습니까?", "success", "취소");
        if (res) {
            let { code, data } = await wiz.call("drive", { "id": this.dataset_id, "name": this.list.title, "docID": this.history.id });
            if (code == 200) {
                await this.alert("저장되었습니다.", "success");
            }
        }
    }

    private async change(mode) {
        if (mode === "list") {
            this.tab = "list";
            this.listMode = "list";
        }
        else if (mode === "share") {
            this.tab = "share";
        }
        else {
            let message = "tab을 바꾸는 과정에서 오류가 발생했습니다. 다시 시도해 주십시오."
            await this.alert(message);
        }
        await this.service.render();
    }

    private async changeMode(item: any) {
        if (this.listMode === "list") {
            this.listMode = "detail";
            this.history = item;

            if (this.history.status == 'request') {
                this.status = "request";
                this.statusContent = "접수되었습니다.";
            } else if (this.history.status == 'process') {
                this.status = "request";
                this.statusContent = this.history.dataset_name + " 데이터셋 활용 가능 여부 심사중입니다.";
            } else if (this.history.status == 'reject') {
                this.status = "request";
                this.statusContent = this.history.dataset_name + " 데이터셋을 활용할 수 없습니다.";
            } else if (this.history.status == 'allow') {
                this.status = "download";
                this.statusContent = this.history.dataset_name + " 데이터셋을 활용할 수 있습니다.";
            }
        }
        else if (this.listMode === "detail") {
            this.listMode = "list";
        }
        else {
            let message = "List의 mode를 바꾸는 과정에서 오류가 발생했습니다. 다시 시도해 주십시오."
            await this.alert(message);
        }
        await this.service.render();
    }

    private async showFilter(filter) {
        let arr = [];
        const getTrueKeys = (obj) => Object.keys(obj).filter(key => obj[key] === true);

        let isEmpty = true;
        for (let key in filter) {
            if (typeof filter[key] === 'object' && filter[key] !== null && Object.keys(filter[key]).length > 0) {
                isEmpty = false;
                let trueKeys = getTrueKeys(filter[key]);
                for (let i = 0; i < trueKeys.length; i++) {
                    if (arr.length >= 5) {
                        break;
                    }
                    arr.push(trueKeys[i]);
                }
            } else if (typeof filter[key] === 'string' && filter[key] !== '') {
                isEmpty = false;
            }

            if (arr.length >= 5) {
                break;
            }
        }
        if (isEmpty) {
            arr.push("전체");
        }
        return arr;
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}