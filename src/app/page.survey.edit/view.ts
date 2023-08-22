import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {

    constructor(
        public service: Service
    ) { }

    public surveyID: any;
    public info = {
        id: "",
        title: "",
        description: "",
        question_file: "",
        answer_file: "",
        created: "",
        updated: ""
    }
    public loadedQ = true;
    public loadedA = true;
    public fileInfo: any;

    public async ngOnInit() {
        await this.service.init();
        if (Object.keys(this.service.auth.session).length === 0 || this.service.auth.session.role != 'admin') {
            this.service.href(`/`);
            return;
        }
        await this.loading(true);
        await this.load();
        await this.loading(false);
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
        this.surveyID = WizRoute.segment.id;
        let { code, data } = await wiz.call("load", { id: this.surveyID });

        if (code != 200) return;
        this.info = data;
        if (this.info.question_file) this.loadedQ = false;
        if (this.info.answer_file) this.loadedA = false;
        await this.service.render();
    }

    public async request() {
        let copy = JSON.stringify(this.info)
        if (!this.info.question_file || this.info.question_file.length==0) {
            await this.alert("설문지 파일을 업로드해주세요.", "error");
            return;
        } else if (!this.info.answer_file || this.info.answer_file.length==0) {
            await this.alert("설문 결과 파일을 업로드해주세요.", "error");
            return;
        }

        if (this.surveyID == "new") {
            let res = await this.alert("설문 분석 요청을 진행하시겠습니까?.", "success", "취소");
            if (res) {
                let { code, data } = await wiz.call("request", { info: copy });
                if (code != 200) return;
                await this.service.href(`/survey`);
                return;
            }
        } else {
            let { code, data } = await wiz.call("request", { info: copy });
            if (code != 200) return;
            await this.alert("저장되었습니다.", "success");
        }
        await this.service.render();
    }

    public async delete() {
        let copy = JSON.stringify(this.info);
        let res = await this.alert("삭제하시겠습니까?", "error", "취소")
        if (res) {
            let { code, data } = await wiz.call("delete", { id: this.surveyID });
            if (code != 200) return;
            this.service.href(`/survey`);
            return;
        }
    }

    public async upload(mode) {
        let files = await this.service.file.select({ accept: '.xls,.xlsx,csv,.pdf' });
        if (files) {
            if (mode == "question") this.loadedQ = false;
            else if (mode == "answer") this.loadedA = false;
        }

        let fd = new FormData();
        let filepath = [];
        let filename = "";
        for (let i = 0; i < files.length; i++) {
            if (!files[i].filepath) files[i].filepath = this.info.id + "/" + files[i].name;
            fd.append('file[]', files[i], files[i].name);
            filename = files[i].name;
            filepath.push(files[i].filepath);
        }
        fd.append("data", JSON.stringify({ data: this.info }));
        fd.append("filepath", JSON.stringify(filepath));

        let url = wiz.url('upload');
        let { code, data } = await this.service.file.upload(url, fd);
        if (code != 200) {
            await this.alert("파일 업로드 중 오류가 발생했습니다")
            return;
        }

        for (let i = 0; i < data.res.length; i++) {
            console.log(data.res[i])
            this.fileInfo = data.res[i];
        }

        if (mode == "question") this.info.question_file = filename;
        else if (mode == "answer") this.info.answer_file = filename;

        await this.service.render();
    }

    public async download(file) {
        let download = wiz.url("download?id=" + this.info.id + "&name=" + file)
        window.location.href = download; // 새창열기 없이 다운로드
    }

    public async removeFile(mode: any, file: any) {
        let { code, data } = await wiz.call("removeFile", { filename: file, surveyID: this.info.id })
        if (code != 200) return
        if (mode == "qusetion") this.loadedQ = false;
        else if (mode == "answer") this.loadedA = false;

        await this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}