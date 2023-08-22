import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';
import { ElementRef, ViewChild } from '@angular/core';

export class Component implements OnInit {
    @Input() list: any = {};

    @ViewChild('editor')
    public editorElement: ElementRef;

    public editor: any;

    public category_ls = {
        "기기": "device",
        "혈자리": "blood",
        "한약재": "herbal",
        "의료기관": "medical",
        "탕약": "decoction"
    };

    public all: any;
    public fileListLoad: boolean = false;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
        await this.buildEditor();
        await this.service.render();
    }

    public async load() {
        this.dataset_id = WizRoute.segment.id;
        let { code, data } = await wiz.call("load", { "id": this.dataset_id });
        this.info = data.dataInfo;
        this.fileInfo = data.fileInfo;
        for (let item of this.fileInfo) {
            if (item.year == "all") this.all = item.rows;
        }
        if (code != 201) {
            this.fileListLoad = true
            this.fileList = data.fileList;
        }
        await this.service.render();
    }

    public async buildEditor() {
        let editor = this.editor = await ClassicEditor.create(this.editorElement.nativeElement, {
            toolbar: {
                items: [
                    'undo', 'redo',
                    '|', 'heading',
                    '|', 'alignment:left', 'alignment:center', 'alignment:right', 'alignment:justify',
                    '|', 'fontColor', 'fontBackgroundColor', 'highlight',
                    '|', 'bold', 'italic', 'strikethrough', 'underline', 'code',
                    '|', 'bulletedList', 'numberedList', 'todoList', 'outdent', 'indent',
                    '|', 'link', 'uploadImage', 'insertTable', 'blockQuote', 'codeBlock'
                ],
                shouldNotGroupWhenFull: true
            },
            heading: {
                options: [
                    { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
                    { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
                    { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
                    { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
                    { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
                    { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
                    { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
                ]
            },
            link: {
                addTargetToExternalLinks: true,
                defaultProtocol: 'https://'
            },
            removePlugins: ["MediaEmbedToolbar", "Markdown"],
            table: ClassicEditor.defaultConfig.table,
            simpleUpload: {
                uploadUrl: '/files/dataset/upload/' + this.category_ls[this.info.category] + "/" + this.info.id
            }
        });

        const toolbarElement = editor.ui.view.toolbar.element;
        toolbarElement.style.display = 'none';
        editor.isReadOnly = true;
        this.editor.data.set(this.info.content);
    }

    public async download(file) {
        let download = wiz.url("download?path=" + file.path + "&name=" + file.name)
        // window.open(download, '_blank');
        window.location.href = download; // 새창열기 없이 다운로드
    }
}