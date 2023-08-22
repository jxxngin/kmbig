import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';

export class Component implements OnInit {

    public docId: any;
    public info = {
        id: "",
        user_id: "",
        user: "",
        category: "",
        title: "",
        dataset_id: "",
        dataset_name: "",
        purpose: "",
        status: "",
        status_class: "",
        status_name: "",
        created: "",
        updated: "",
        deadline: ""
    };
    public userID: any;

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

    constructor(
        public service: Service,
        private router: Router
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.userID = this.service.auth.session.id;

        await this.load();

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.currentRoute = event.url;
                if (this.currentRoute.includes("/share/user/form/view")) {
                    await this.load();
                }
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
        this.docId = WizRoute.segment.id;
        let { code, data } = await wiz.call("load", { id: this.docId });
        if (code == 300) {
            this.service.href(`/share/user/form`);
            return;
        }
        this.info = data;
        if (this.info.filter) {
            this.filter = JSON.parse(this.info.filter.replace(/'/g, '"').replace(/True/g, 'true').replace(/False/g, 'false'));
        };
        await this.service.render();
    }

    public async download() {
        // let download = wiz.url('download?id=' + this.info.dataset_id + "&title=" + this.info.dataset_name + "&user=" + this.userID)
        // window.open(download, '_blank');
        let download = wiz.url('download?id=' + this.info.dataset_id + "&title=" + this.info.dataset_name + "&docID=" + this.docId)
        window.location.href = download;
    }

    public async drive() {
        let res = await this.alert(this.info.dataset_name + " 데이터셋을 연구자 서랍에 저장하시겠습니까?", "success", "취소");
        if (res) {
            let { code, data } = await wiz.call("drive", { "id": this.info.dataset_id, "name": this.info.dataset_name, "docID": this.docId });
            if (code == 200) {
                await this.alert("저장되었습니다.", "success");
            }
        }
    }
}