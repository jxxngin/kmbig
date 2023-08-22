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
            labels: ['우유', '계란흰자', '복숭아', '바퀴벌레', '콩', '고양이', '개', '새우', '게', '감자'],
            datasets: [{
                label: '데이터 상세보기',
                data: [80, 50, 40, 35, 30, 25, 20, 10, 5, 2],
                backgroundColor: [
                    '#4F40F1',
                    '#9996B7',
                    '#DFDEF7'
                ],
                borderColor: [
                    '#4F40F1',
                    '#9996B7',
                    '#DFDEF7'
                ],
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
        };

        // const ctx = document.getElementById('widget-bar-many').getContext('2d');
        // let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}