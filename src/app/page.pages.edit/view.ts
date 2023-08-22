import { OnInit, ElementRef, ViewChild } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { ActivatedRoute, Router, Event, NavigationEnd } from '@angular/router';
import { CKEditorModule } from '@ckeditor/ckeditor5-angular';
import * as ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {
    public editorElement: ElementRef;
    public editor: any;
    public Editor = ClassicEditor;

    public info = {
        id: "",
        pages: "",
        content: ""
    };
    private category = "";

    constructor(
        public service: Service,
        public route: ActivatedRoute,
        public router: Router
    ) { }

    public async ngOnInit() {
        // await this.service.init();
        let init = await this.service.init();
        if (Object.keys(init.auth.session).length === 0 || init.auth.session.role != "admin") {
            this.service.href(`/`);
            return;
        }
        this.category = WizRoute.segment.category;
        await this.load();
        await this.service.render();
        // await this.load(this.category);
        // await this.service.render();

        // this.route.url.subscribe(async ([_, __, { path }]) => {
        //     await this.load(path);
        //     await this.service.render();
        // })

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.category = WizRoute.segment.category;
                await this.load();
                await this.service.render();
            }
        })
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

    // public async load(category) {
    public async load() {
        if (this.category === undefined) {
            return;
        }
        // let { code, data } = await wiz.call("load", { "category": category });
        let { code, data } = await wiz.call("load", { "category": this.category });
        if (code !== 200) {
            return;
        }
        this.info = data;

        const EDITOR_ID = `textarea#editor`;
        this.editor = await ClassicEditor.create(document.querySelector(EDITOR_ID), {
            toolbar: {
                items: 'heading | bold italic strikethrough underline | fontColor highlight fontBackgroundColor | bulletedList numberedList todoList | outdent indent | insertTable imageUpload | link blockQuote code codeBlock'.split(' '),
                shouldNotGroupWhenFull: true
            },
            removePlugins: ["MediaEmbedToolbar", "Markdown"],
            table: ClassicEditor.defaultConfig.table,
            simpleUpload: {
                uploadUrl: '/file/page/upload/' + this.info.pages
            }
        });
        this.editor.data.set(this.info.content);
    }

    public async save() {
        let info = this.info;
        info.content = this.editor.data.get();
        let { code, data } = await wiz.call("save", this.info);
        if (code == 200) {
            await this.alert("저장되었습니다.", 'success');
        }
    }
}