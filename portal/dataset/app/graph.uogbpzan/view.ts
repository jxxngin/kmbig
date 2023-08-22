import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

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
            this.dataset_id = "hcaiajhxaBmT4SSN0eXqHckUab1TEEQD";
        }
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        if (code == 200) {
            this.labels = data.labels;
            this.weight = data.weight_means;
            this.bmi = data.bmi_means;
        }
        await this.service.render();
    }

    public async loadGraph() {
        const data = {
            labels: this.labels,
            datasets: [{
                // label: '데이터 상세보기',
                data: this.weight,
                backgroundColor: [
                    'rgb(242, 116, 141, 0.2)'
                ],
                borderColor: [
                    '#F2748D'
                ],
                fill: true,
                pointBackgroundColor: '#fff',
                borderWidth: 3,
            }, {
                data: this.bmi,
                backgroundColor: [
                    'rgb(79, 64, 241, 0.2)'
                ],
                borderColor: [
                    '#4F40F1'
                ],
                fill: true,
                pointBackgroundColor: '#fff',
                borderWidth: 3,
                yAxisID: 'y2'
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: false,
                maxBarThickness: 40,
                plugins: {
                    legend: {
                        display: false,
                    },
                    datalabels: {
                        display: false,
                    }
                },
                scales: {
                    y: {
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: {
                            stepSize: 25
                        },
                        title: {
                            display: true,
                            text: '몸무게(kg)'
                        }
                    },
                    y2: {
                        suggestedMin: 0,
                        suggestedMax: 30,
                        ticks: {
                            stepSize: 5
                        },
                        title: {
                            display: true,
                            text: 'BMI'
                        },
                        position: 'right'
                    },
                    x: {
                        title: {
                            display: true,
                            text: '신장(cm)'
                        }
                    }
                }
            },
        };

        const ctx = document.getElementById('widget-whb').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}