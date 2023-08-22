import { OnInit, ViewChild, ElementRef } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {

    public formID: any;
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
        expert_status: "",
        status_class: "",
        status_name: "",
        created: "",
        updated: "",
        deadline: "",
        comment: ""
    };
    public preview = {
        df: "",
        graph: "",
        schema: ""
    }

    @ViewChild('editor')
    public editorElement: ElementRef;

    public editor: any;
    public editorLoaded: boolean = false;

    public expertID: any;

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
    public previewTF: boolean = true;

    constructor(
        public service: Service,
        private router: Router
    ) { }

    public async ngOnInit() {
        let init = await this.service.init();
        if (Object.keys(init.auth.session).length === 0 || init.auth.session.is_expert == 0) {
            this.service.href(`/`);
            return;
        }
        this.expertID = init.auth.session.id;
        await this.load();

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.currentRoute = event.url;
                if (this.currentRoute.includes("/share/expert/form/view")) {
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
        this.formID = WizRoute.segment.id;
        let { code, data } = await wiz.call("load", { id: this.formID });
        if (code == 300) {
            this.service.href(`/share/expert/form`);
            return;
        }
        this.info = data.info;
        this.info.created = this.info.created.substring(0, 10);
        if (this.info.filter) {
            this.filter = JSON.parse(this.info.filter.replace(/'/g, '"').replace(/True/g, 'true').replace(/False/g, 'false'))
        }
        this.preview = data.preview;
        this.preview.schema = JSON.parse(data.preview.schema)
        if (this.preview.df.length == 0) {
            this.previewTF = false;
        } else {
            this.previewTF = true;
            this.columns = [];
            for (let value of this.preview.df) {
                for (let key in value) {
                    if (!this.columns.includes(key)) {
                        this.columns.push(key);
                    }
                }
            }
        }

        await this.service.render();
        if ((['allow', 'reject', 'stop'].includes(this.info.expert_status) && this.info.comment != '') || this.info.expert_status == 'process') {
            await this.buildEditor();
        }
        await this.service.render();
    }

    // 데이터셋 정보(상세 설명) 페이지 이동
    public async open() {
        this.url = "https://kmbig.seasonsoft.net/dashboard/device/" + this.info.dataset_id;
        window.open(this.url)
    }

    // 공유 활용 거절
    public async reject() {
        let comment = this.editor.data.get();
        let res = await this.alert(this.info.dataset_name + " 활용 요청을 거절하시겠습니까?", "error", "취소");
        if (res) {
            await this.loading(true);
            let { code, data } = await wiz.call("update", { form: this.formID, comment: comment, status: "reject" });
            if (code == 200) {
                await this.loading(false);
                location.reload();
            }
        }
    }

    // 공유 활용 승인
    public async allow() {
        let comment = this.editor.data.get();
        let res = await this.alert(this.info.dataset_name + " 활용 요청을 승인하시겠습니까?", "success", "취소");
        if (res) {
            await this.loading(true);
            let { code, data } = await wiz.call("update", { form: this.formID, comment: comment, status: "allow" });
            if (code == 200) {
                await this.loading(false);
                location.reload();
            }
        }
    }

    public isEditable() {
        if (['allow', 'reject', 'stop'].includes(this.info.expert_status)) {
            return false;
        } else {
            return true;
        }
    }

    public async buildEditor() {
        this.editorLoaded = false;
        await this.service.render();
        this.editorLoaded = true;
        await this.service.render();
        let editor = this.editor = await ClassicEditor.create(this.editorElement.nativeElement, {
            toolbar: {
                shouldNotGroupWhenFull: true
            },
            link: {
                addTargetToExternalLinks: true,
                defaultProtocol: 'https://',
            },
            removePlugins: ["MediaEmbedToolbar", "Markdown"],
            table: ClassicEditor.defaultConfig.table,
            simpleUpload: {
                uploadUrl: 'files/expert/upload/dataset/' + this.info.id + '/' + this.info.expert + '/' + this.info.dataset_id
            }
        });

        if (!this.isEditable()) {
            const toolbarElement = editor.ui.view.toolbar.element;
            toolbarElement.style.display = 'none';
            editor.isReadOnly = true;
        }
        this.editor.data.set(this.info.comment);
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}