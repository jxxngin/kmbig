import { OnInit } from '@angular/core';
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
        if (!this.dataset_id) {
            this.dataset_id = "k1pkjQJFhmmC9sSXCt23g4SAvKYtVDp1";
        }
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        this.labels = data.label;
        this.datas = data.value;
        this.colors = ['#3E1FEC', '#7E6DF4', '#686599', '#7775A5', '#8886B0', '#A9A9C8', '#B9B9D2', '#C8C8DC', '#D8D8E6', '#E8E8F0'];
        await this.service.render();
    }

    public async loadGraph() {
        const data = {
            labels: this.labels,
            datasets: [{
                label: '알레르기 비율',
                data: this.datas,
                backgroundColor: this.colors,
                borderColor: this.colors,
                borderWidth: 1,
                borderRadius: 7,
            }]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: false,
                maxBarThickness: 40,
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
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: {
                            stepSize: 25
                        }
                    }
                }
            },
            plugins: [ChartDataLabels],
        };

        const ctx = document.getElementById('widget-allergy').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}