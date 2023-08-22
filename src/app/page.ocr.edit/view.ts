import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import toastr from "toastr";
toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": true,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": 300,
    "hideDuration": 500,
    "timeOut": 1500,
    "extendedTimeOut": 1000,
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

export class Component implements OnInit {
    constructor(
        public service: Service,
    ) { }

    private page = {
        current: 0,
        last: 1,
    };

    public ocrID: any;
    public info = {
        id: "",
        name: "새로운 설문",
    }
    public list = [];
    private file = [];
    private images = [];
    private settingIndex = -1;

    public async ngOnInit() {
        await this.service.init();
        if (Object.keys(this.service.auth.session).length === 0 || this.service.auth.session.role != 'admin') {
            this.service.href(`/`);
            return;
        }
        await this.loading(true);
        // via init
        await _via_init();

        this.ocrID = WizRoute.segment.id;
        if (this.ocrID !== 'new')
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

    private async init() {
        let info = JSON.stringify(this.info)

        let { code, data } = await wiz.call("init", { name: this.info.name });
        if (code !== 200) return;

        this.ocrID = data;

        await this.load();
    }

    public async load() {
        let { code, data } = await wiz.call("load", { id: this.ocrID });
        if (code != 200) return;

        this.info = data.info;
        this.list = data.data;

        if (this.info.file) {
            this.file = this.info.file;
            this.images = JSON.parse(this.info.images);
            await this.show();
        }

        // console.log(this.list)

        await this.service.render();
    }

    private async fileSelect(event) {
        this.file = event.target.files[0];
    }

    private async upload() {
        if (this.file.length === 0) {
            let message = "파일을 선택해주세요.";
            await this.alert(message);
            return;
        }

        await this.loading(true);

        let file = this.file;
        let fd = new FormData();

        if (!file.filepath) file.filepath = "ocr/" + this.ocrID + "/pdf";
        if (!file.filename) file.filename = file.name;
        fd.append("file[]", file);
        fd.append("filepath", JSON.stringify(file.filepath));
        fd.append("filename", JSON.stringify(file.filename));

        let url = wiz.url("upload");
        await this.service.file.upload(url, fd);

        await this.pdfToImg();
    }

    private async pdfToImg() {
        const { code, data } = await wiz.call("pdf", { id: this.ocrID, name: this.file.name });
        if (code !== 200) {
            let message = "pdf 변환 과정에서 오류가 발생했습니다. 다시 시도해주세요.";
            await this.alert(message);
            return;
        }
        this.images = data.images;
        this.page.last = data.lastPage;

        await this.loading(false);
        await this.load();
    }

    private async show() {
        const page = this.page.current;
        let input = { url: { value: '' }, url_list: {} };
        let src = [];
        for (let i = 0; i < this.images.length; i++) {
            let fullPath = this.images[i];
            let slashIndex = fullPath.lastIndexOf('/');

            let path = fullPath.substring(0, slashIndex);
            let name = fullPath.substring(slashIndex + 1);

            src[i] = wiz.url("download?path=" + path + "&name=" + name);
        }
        input.url_list.value = src.join("\n");
        project_file_add_url_input_done(input);

        await this.service.render();
    }

    public async addQ() {
        if (this.list == null || this.list.length == 0) {
            this.list = [];
        }
        let data = {
            question_id: "",
            question_sub: "",
            question_name: "",
            result: "",
            pos: "",
        };
        this.list.push(data);
        await this.service.render();
    }

    public async deleteQ(index) {
        if ("id" in this.list[index]) {
            let { code } = await wiz.call("deleteQ", { qID: this.list[index].id });
            if (code != 200) return;
        }
        this.list.splice(index, 1);
        await this.alert("삭제되었습니다.", "error");
        await this.service.render();
    }

    public async request() {
        let copy = JSON.stringify(this.info);
        let copy2 = JSON.stringify(this.list);

        let { code } = await wiz.call("request", { id: this.ocrID, info: copy, list: copy2 });
        if (code != 200) return;

        await this.alert("저장되었습니다.", "success");
        await this.load();
    }

    public async remove() {
        let res = await this.alert("삭제하시겠습니까?", "error", "취소")
        if (res) {
            let { code } = await wiz.call("remove", { id: this.ocrID });
            if (code != 200) return;
            this.service.href("/ocr/list");
        }
    }

    private async setting(index) {
        sel_all_regions();
        del_sel_regions();

        if (this.settingIndex == index) {
            this.settingIndex = -1;
            document.getElementById('VIA').style.opacity = 0;
            document.getElementById('VIA').style.visibility = 'hidden';
            await this.service.render();
            return;
        }

        this.settingIndex = index;
        document.getElementById('VIA').style.opacity = 1;
        document.getElementById('VIA').style.visibility = 'visible';

        let data = this.list[index].pos;
        if (data.length > 0) {
            let dataObj = JSON.parse(data);
            let imageIndex;

            for (let key in dataObj._via_img_metadata) {
                let regions = dataObj._via_img_metadata[key].regions;

                for (let i = 0; i < regions.length; i++) {
                    let shape_attributes = regions[i].shape_attributes;
                    let res = wiz.url("download?path=/var/www/kmbig_admin/storage/ocr/" + this.ocrID + "/" + key);

                    if (_via_img_metadata[res + "-1"]) {
                        _via_img_metadata[res + "-1"].regions.push({ shape_attributes: shape_attributes, region_attributes: {} });
                        imageIndex = Object.keys(_via_img_metadata).indexOf(res + "-1");
                    }
                }
            }
            if (imageIndex !== undefined) {
                _via_image_index = imageIndex;
            }

            _via_show_img(_via_image_index);
        }

        await this.service.render();
    }

    private async apply() {
        let res = await this.alert("적용하시겠습니까?");
        if (!res) {
            return;
        }
        document.getElementById('VIA').style.opacity = 0;
        document.getElementById('VIA').style.visibility = 'hidden';
        // via
        let via = project_save_with_confirm();
        const data = JSON.parse(via);
        const files = Object.keys(data._via_img_metadata);

        let page = 0;
        let result = 0;

        for (let i = 0; i < files.length; i++) {
            const regions = data._via_img_metadata[files[i]].regions;
            result = regions.length;

            if (result > 0) {
                let pageString = files[i].split('_').pop().split('.png')[0];
                page = parseInt(pageString, 10);

                this.list[this.settingIndex].result = result;
                this.list[this.settingIndex].page = page;
                this.list[this.settingIndex].pos = via;

                sel_all_regions();
                del_sel_regions();

                await this.service.render();
                return;
            }
        }
        this.settingIndex = -1;
        await this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}
