import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private page = {
        current: 1,
        last: 1,
    };

    private ocr = {
        id: "",
        info: {},
        data: {},
    };

    private files = [];
    private fileIndex = 0;

    private showFiles = false;
    private showResult = false;
    private saveall = false;

    private images = [];
    private src = "";

    private list = [];
    private result = [];
    private name = [];

    private _loading = false;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();

        if (Object.keys(this.service.auth.session).length === 0) {
            this.service.href(`/`);
            return;
        }
        this.ocr.id = WizRoute.segment.id;

        await this.load();
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

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }

    private async load() {
        const { code, data } = await wiz.call("load", { id: this.ocr.id });
        if (code !== 200) {
            let message = "설문 유형을 불러오는 과정에서 오류가 발생했습니다. 다시 시도해주세요.";
            await this.alert(message);
            return;
        }

        this.ocr.info = data.info;
        this.ocr.data = data.data;

        await this.service.render();
    }

    private async upload() {
        let files = await this.service.file.select({ accept: '.pdf', multiple: true });

        if (files.length === 0) {
            let message = "파일을 1개 이상 업로드 해주세요.";
            await this.alert(message);
            return;
        }

        this.showFiles = true;
        this.files = files;

        await this.service.render();
    }

    private async deleteFile(file, i) {
        let res = await this.service.alert.show({
            title: "",
            message: file.name + "을 삭제하시겠습니까?",
            action: "Delete",
            cancel: "취소",
        });

        if (!res) {
            return;
        }

        const df = new DataTransfer();

        let fileArr = Array.from(this.files);
        fileArr.splice(i, 1);
        fileArr.forEach(item => { df.items.add(item); });

        this.files = df.files;

        await this.service.render();
    }

    private async start() {
        if (this.files.length === 0) {
            let message = "파일을 선택해주세요.";
            await this.alert(message);
            return;
        }

        this.showResult = true;

        // ocr data setting
        for (let i = 0; i < this.ocr.data.length; i++) {
            if (this.ocr.data[i].pos) {
                let data = JSON.parse(this.ocr.data[i].pos);
                for (let key in data._via_img_metadata) {
                    let regions = data._via_img_metadata[key].regions;
                    if (regions.length > 0) {
                        this.ocr.data[i].pos = regions;
                        break;
                    }
                }
            }

        }
        await this.setFile(this.fileIndex);
    }

    private async setFile(index) {
        if (!this.saveall) await this.loading(true);
        this.page.current = 1;

        let file = this.files[0];
        let fd = new FormData();

        if (!file.filepath) file.filepath = "ocr/" + this.ocr.id + "/analysis";
        if (!file.filename) file.filename = file.name;
        fd.append("file[]", file);
        fd.append("filepath", JSON.stringify(file.filepath));
        fd.append("filename", JSON.stringify(file.filename));

        let url = wiz.url("upload");
        await this.service.file.upload(url, fd);

        await this.pdfToImg(file);
    }

    private async pdfToImg(file) {
        const { code, data } = await wiz.call("pdf", { id: this.ocr.id, name: file.name });
        if (code !== 200) {
            let message = "pdf 변환 과정에서 오류가 발생했습니다. 다시 시도해주세요.";
            await this.alert(message);
            return;
        }
        this.images = data;
        this.page.last = data.length;
        if (!this.saveall) await this.loading(false);
        await this.show();
    }

    private async show() {
        const page = this.page.current;
        let fullPath = this.images[page - 1];
        let slashIndex = fullPath.lastIndexOf('/');

        let path = fullPath.substring(0, slashIndex);
        let name = fullPath.substring(slashIndex + 1);
        this.src = wiz.url("download?path=" + path + "&name=" + name);

        await this.setList();
    }

    private async setList() {
        this.list = [];
        for (let i = 0; i < this.ocr.data.length; i++) {
            if (this.page.current === this.ocr.data[i].page) {
                this.list.push(this.ocr.data[i]);
            }
        }

        const posList = this.list.map(item => {
            if (item.pos) {
                return item.pos.map(posItem => {
                    let { x, y, width: w, height: h } = posItem.shape_attributes;
                    return { x, y, w, h };
                });
            }
        });

        await this.getBox(posList);
    }

    private async getBox(list) {
        const result = [];
        const canvas = document.getElementById("ocr");
        const img = new Image();
        img.src = this.src;

        await new Promise(resolve => {
            img.onload = async () => {
                canvas.width = img.width;
                canvas.height = img.height;

                const ctx = canvas.getContext("2d");
                ctx.strokeStyle = "red";
                ctx.drawImage(img, 0, 0);


                list.forEach((row, rowIndex) => {
                    if (row === undefined)
                        return
                    let checkIndex = [];
                    row.forEach((pos, posIndex) => {
                        const { x, y, w, h } = pos;
                        ctx.strokeRect(x, y, w, h);
                        let data = ctx.getImageData(x, y, w, h).data;

                        let cnt = 0;
                        let total = 0;
                        for (let i = 0; i < data.length; i += 4) {
                            const avg = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
                            total++;
                            if (avg >= 250)
                                cnt++;
                        }
                        // console.log(cnt / total)
                        if (cnt / total < 0.5) {
                            checkIndex.push(posIndex + 1);
                        }
                    });
                    result.push({ ...checkIndex });
                });
                await this.setCheck(result);
                resolve();
            };
        });
    }

    private async setCheck(data) {
        let index = 0;
        this.list.forEach(item => {
            if (item.result !== 0) {
                let answers = data[index];
                let res = Array(item.result).fill(false);

                for (let key in answers) {
                    let idx = answers[key];
                    res[idx - 1] = true;
                }

                item.answer = res;
                index++;
            }
        });
        await this.service.render();
    }

    private async prev() {
        this.page.current--;
        await this.show();
    }

    private async next() {
        if (!this.result[this.fileIndex]) {
            this.result[this.fileIndex] = [];
        }

        if (this.list.length !== 0) {
            for (let i = 0; i < this.list.length; i++) {
                if (!this.result[this.fileIndex].includes(this.list[i])) {
                    this.result[this.fileIndex].push(this.list[i]);
                }
            }
        }

        if (this.page.current !== this.page.last) {
            this.page.current++;
            await this.show();
        }
    }

    private async showAll() {
        for (let i = this.page.current; i <= this.page.last; i++) {
            await this.next();
        }
    }

    private async download() {
        let res = await this.service.alert.show({
            title: "",
            message: "저장하면 설문 결과를 수정할 수 없습니다. 정말로 엑셀 저장을 하시겠습니까?",
            action: "Save",
            cancel: "취소",
        });
        if (!res) return;

        await this.loading(true);
        this.saveall = true;

        for (let i = this.fileIndex; i < this.files.length; i++) {
            await this.showAll();

            let filename = this.files[this.fileIndex].name;
            filename = filename.substring(filename.lastIndexOf('_') + 1, filename.lastIndexOf('.'));
            if (!this.name.includes(filename)) {
                this.name.push(filename);
            }

            if (this.fileIndex < this.files.length - 1) {
                this.fileIndex++;
                await this.setFile(this.fileIndex);
            }
        }

        console.log(this.result)
        console.log(this.name)

        await this.loading(false);
        await this.excel();

        let message = "모든 설문이 저장되었습니다!";
        await this.alert(message);

        const { code } = await wiz.call("finish", { id: this.ocr.id });
        location.reload();
    }

    private async excel() {
        let result = JSON.stringify(this.result);
        let name = JSON.stringify(this.name);

        const { code, data } = await wiz.call("excel", { id: this.ocr.id, result, name });
        if (code !== 200) {
            let message = "엑셀 변환 과정에서 오류 발생";
            await this.alert(message);
            return;
        }

        let download = wiz.url("download?path=" + data.filepath + "&name=" + data.filename);
        window.open(download, '_blank');
    }

    private async nextFile() {
        await this.next();

        let filename = this.files[this.fileIndex].name;
        filename = filename.substring(filename.lastIndexOf('_') + 1, filename.lastIndexOf('.'));
        if (!this.name.includes(filename)) {
            this.name.push(filename);
        }

        if (this.fileIndex < this.files.length - 1) {
            let res = await this.service.alert.show({
                title: "",
                message: "다음 파일을 보시겠습니까?",
                action: "Yes",
                cancel: "No",
            });
            if (!res) return;

            this.fileIndex++;
            await this.setFile(this.fileIndex);
        }
        else {
            let message = "마지막 파일 입니다";
            await this.alert(message);
        }
    }

    public filesize(value) {
        if (!value) return "--";
        let kb = value / 1024;
        if (kb < 1) return value + "B";
        let mb = kb / 1024;
        if (mb < 1) return Math.round(kb * 100) / 100 + "KB";
        let gb = mb / 1024;
        if (gb < 1) return Math.round(mb * 100) / 100 + "MB";
        return Math.round(gb * 100) / 100 + "GB";
    }
}