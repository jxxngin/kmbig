import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    // @Input() title: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        const data = {
            labels: ['155','160','165','170','175','180','185','190','195','200', '215','220','225','230','235'],
            datasets: [{
                // label: '데이터 상세보기',
                data: [12, 20, 25, 52, 60, 80, 72, 85, 85, 75, 72, 62, 60, 47, 45, 30],
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
                data: [12, 40, 48, 38, 35, 55, 30, 52, 50, 30, 95, 47, 38, 28, 72, 60],
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
                        suggestedMax: 100,
                        ticks: {
                            stepSize: 25
                        },
                        title: {
                            display: true,
                            text: '대사량(kcal)'
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

        const ctx = document.getElementById('widget-line').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}