import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';

export class Component implements OnInit {

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loadFile();
        await this.loadGraph();
    }

    public async loadFile() {
        this.dataset_id = WizRoute.segment.id;
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        if (code == 200) {
            this.files = data;
            this.datas = [];
            this.labels = [];
            for (let file of this.files) {
                this.labels.push(file.year)
                this.datas.push(file.rows)
            }
        }

        await this.service.render();
    }

    public async loadGraph() {
        const data = {
            labels: this.labels,
            datasets: [{
                label: "데이터 건수",
                data: this.datas,
                backgroundColor: [
                    '#4F40F1',
                    '#B0B0E8',
                    '#C9C5F0',
                    '#DFDEF7'
                ],
                borderColor: [
                    '#4F40F1',
                    '#B0B0E8',
                    '#C9C5F0',
                    '#DFDEF7'
                ],
                borderWidth: 1,
                borderRadius: 7,
            }]
        };

        let maxValue = Math.max(...this.datas);
        let roundUnit;

        if (maxValue > 10000) {
            roundUnit = 10000;
        } else if (maxValue > 1000) {
            roundUnit = 1000;
        } else if (maxValue > 100) {
            roundUnit = 100;
        } else {
            roundUnit = 10;
        }

        maxValue = Math.ceil(maxValue / roundUnit) * roundUnit + roundUnit;

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: false,
                maxBarThickness: 100,
                plugins: {
                    legend: {
                        display: false,
                    },
                    datalabels: {
                        color: '#6F6F6F',
                        align: '-90',
                        anchor: 'end',
                    },
                },
                scales: {
                    y: {
                        max: maxValue
                    }
                }
            },
            plugins: [ChartDataLabels],
        };

        const ctx = document.getElementById('widget-bar-yearly').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}