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
            labels: ['우로빌리노겐','포도당','빌리루빈','케론체','요비중','잠혈','Ph','요단백','요아질산염','백혈구'],
            datasets: [{
                label: '데이터 상세보기',
                data: [40, 87, 60, 20, 52, 10, 30, 72, 52, 70],
                backgroundColor: [
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1'
                ],
                borderColor: [
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1',
                    '#4F40F1'
                ],
                borderWidth: 1,
                borderRadius: 10,
            }]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                indexAxis: 'y',
                responsive: false,
                maxBarThickness: 15,
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

        const ctx = document.getElementById('widget-bar-left').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}