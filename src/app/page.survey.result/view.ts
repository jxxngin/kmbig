import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';
import { DomSanitizer } from '@angular/platform-browser';

export class Component implements OnInit {

    constructor(
        public service: Service,
        private sanitizer: DomSanitizer,
    ) { }

    public userRole: any;
    public surveyID: any;
    public color = ['#7329FF', '#0064FF', '#47CCFF', '#24E0A6', '#FF6C00', '#FFC247']
    // public showResult: any;
    public tryExcept = 200;
    public survey: any;
    public previewFile: any;

    public page = 0;
    public total = 0;
    public current = {
        groupID: "",
        content: "",
        note: "",
        data: ""
    };

    public hospital = [
        { name: "가천대학교 한방병원", id: "GC", count: 0 },
        { name: "부산대학교 한방병원", id: "PS", count: 0 },
        { name: "나주 동신대학교 한방병원", id: "DS", count: 0 },
        { name: "동국대학교 한방병원", id: "DG", count: 0 },
        { name: "대전대학교 한방병원", id: "DJ", count: 0 }
    ]
    public hospitalIDs = [];
    public hospitalCount = [];

    public years = [
        { name: "2020", id: "20-", count: 0 },
        { name: "2021", id: "21-", count: 0 },
        { name: "2022", id: "22-", count: 0 }
    ]
    public yearIDs = [];
    public yearCount = [];

    public charts = [];
    public word = "";
    public groupIDs: any;
    public filtered = [];
    public currentIndex = null;

    public PDF: any = "";

    public async ngOnInit() {
        // init 이전에 값 넣어보기
        await this.service.init();
        this.surveyID = WizRoute.segment.id;
        if (Object.keys(this.service.auth.session).length === 0) {
            this.service.href(`/`);
            return;
        }
        this.userRole = this.service.auth.session.role;
        for (let item of this.hospital) {
            this.hospitalIDs.push(item.id);
        }
        for (let item of this.years) {
            this.yearIDs.push(item.id);
        }
        await this.service.render();
        await this.loading(true);
        await this.load();
        await this.service.render();
        await this.loading(false);
    }

    public async load() {
        let copy = JSON.stringify(this.hospitalIDs)
        let copy2 = JSON.stringify(this.yearIDs)
        let { code, data } = await wiz.call("load", { id: this.surveyID, hospitalIDs: copy, yearIDs: copy2 });
        this.tryExcept = code;
        if (code != 200) return;

        this.previewFile = data.preview;
        this.survey = data.result;
        this.groupIDs = data.groups;
        this.hospitalCount = data.count;
        for (let i = 0; i < this.hospitalCount.length; i++) {
            this.hospital[i]["count"] = this.hospitalCount[i];
        }
        this.yearCount = data.count2;
        for (let i = 0; i < this.yearCount.length; i++) {
            this.years[i]["count"] = this.yearCount[i];
        }

        this.total = this.survey.length - 1;

        await this.preview();
        await this.analysis();
        await this.service.render();
    }

    public async preview() {
        let url = wiz.url('pdf');
        url = `${url}?id=${this.surveyID}&file=${this.previewFile}`;
        let fullUrl = `https://kmbig.seasonsoft.net${url}`
        this.PDF = this.sanitizer.bypassSecurityTrustResourceUrl(fullUrl);
        await this.service.render();
    }

    public async analysis() {
        let item = this.survey[this.page];
        await this.service.render();
        this.current = item;
        await this.service.render();
        for (let i = 0; i < item.content.length; i++) {
            if (item.note[i][0] == 'NONE') {
                item.note[i].shift()
                item.data[i].shift()
                await this.service.render();
            }

            let color = this.color.sort(() => Math.random() - 0.5);
            if (item.groupID == "QS05.소변") {
                color = ['#F8F6D2', '#FFFBBA', '#FFF772', '#FEF428', '#FFED5C', '#FEEA2F', '#D6B866', '#8A7934'];
            }


            const modifiedLabels = item.note[i].map(label => {
                if (label.length > 5) {
                    return label.slice(0, 5) + '...';
                }
                return label;
            });

            let graph = {
                labels: modifiedLabels,
                datasets: [{
                    data: item.data[i],
                    backgroundColor: color,
                    borderColor: color,
                    borderWidth: 1
                }]
            };

            let graphType = "";
            let positionType = "right";
            if (item.note[i].length == 1) graphType = "pie"
            else if (item.note[i].length == 2) graphType = "doughnut"
            else if (item.note[i].length >= 3 && item.note[i].length <= 5) graphType = "polarArea";
            else {
                graphType = "bar";
                positionType = "bottom";
            }
            
            let config = {
                type: graphType,
                data: graph,
                options: {
                    responsive: false,
                    plugins: {
                        legend: {
                            onClick: null,
                            position: positionType,
                            maxWidth: 300,
                            labels: {
                                boxWidth: 10,
                                padding: 15,
                                generateLabels: function (chart) {
                                    // const labels = chart.data.labels;
                                    const labels = item.note[i];
                                    const dataset = chart.data.datasets[0];
                                    const total = dataset.data.reduce((a, b) => a + b, 0);
                                    if (total == 0) {
                                        return labels.map((label, index) => {
                                            const percentage = 0;
                                            return {
                                                text: ` ${label}:   ${percentage}%`,
                                                fillStyle: dataset.backgroundColor[index]
                                            };
                                        });
                                    } else {
                                        return labels.map((label, index) => {
                                            const value = dataset.data[index];
                                            const percentage = ((value / total) * 100).toFixed(2);
                                            return {
                                                text: ` ${label} :   ${percentage}%`,
                                                fillStyle: dataset.backgroundColor[index]
                                            };
                                        });
                                    }
                                }
                            },
                        }
                    }
                },
            };

            let ctx = document.getElementById('widget-survey-process-' + this.page + "-" + i).getContext('2d');
            let myChart = new Chart(ctx, config);
            this.charts.push(myChart)
        }
        // await this.service.render();
    }

    public async next() {
        this.page = this.page + 1;
        await this.analysis();
    }

    public async prev() {
        this.page = this.page - 1;
        await this.analysis();
    }

    public async search() {
        let index = this.groupIDs.indexOf(this.word);
        if (index == -1) {
            await this.alert("풀네임으로 검색해주세요", "error");
            return;
        }
        this.page = index;
        this.word = "";
        this.filtered = [];
        await this.analysis();
    }

    public async doSearch() {
        if (this.word) {
            this.filtered = this.groupIDs.filter((item) => item.includes(this.word));
            await this.service.render();
        }
    }

    public async onClick(idx) {
        this.word = this.filtered[idx];
        await this.search();
    }

    public async currentSearch(idx) {
        this.currentIndex = idx;
        await this.service.render();
    }

    public async select(mode, item) {
        if (mode == "hospital") {
            if (this.hospitalIDs.includes(item)) {
                this.hospitalIDs = this.hospitalIDs.filter((element) => element !== item);
            } else {
                this.hospitalIDs.push(item)
            }
        } else {
            if (this.yearIDs.includes(item)) {
                this.yearIDs = this.yearIDs.filter((element) => element !== item);
            } else {
                this.yearIDs.push(item)
            }
        }

        this.charts.forEach(obj => {
            obj.destroy();
        })
        this.charts = [];
        await this.service.render();
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

    public async downloadExcel() {
        let download = wiz.url('download?id=' + this.surveyID + "&title=" + this.info.survey_name)
        window.open(download, '_blank');
    }

    public async downloadImage() {
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }

    private async onKeyDown(event: KeyboardEvent) {
        let key = event.key;
        let len = this.filtered.length;

        switch (key) {
            case "ArrowDown":
                if (this.currentIndex === null) {
                    this.currentIndex = 0;
                }
                else {
                    if (this.currentIndex === len - 1) {
                        this.currentIndex === null;
                    }
                    else {
                        this.currentIndex = (this.currentIndex + len + 1) % len;
                    }
                }
                break;

            case "ArrowUp":
                if (this.currentIndex === null) {
                    this.currentIndex = len - 1;
                }
                else {
                    if (this.currentIndex === 0) {
                        this.currentIndex = null;
                    }
                    else {
                        this.currentIndex = (this.currentIndex + len - 1) % len;
                    }
                }
                break;

            case "Escape":
                document.activeElement.blur();
                return;

            case "Enter":
                if (event.isComposing)
                    return;
                if (this.currentIndex != null)
                    this.word = this.filtered[this.currentIndex];
                this.currentIndex === null;
                await this.search();
                break;

            default:
                return;
        }

        let target = document.querySelectorAll(".autocomplete-item")[this.currentIndex];
        if (target && target.scrollIntoView) {
            target.scrollIntoView(false);
        }
        await this.service.render();
    }
}