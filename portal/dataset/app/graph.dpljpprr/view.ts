import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    private mode = "lightred"
    private tongue = [
        { id: "lightred", name: "담홍지수" },
        { id: "coated", name: "설태지수" },
        { id: "bluepurple", name: "청자지수" },
        { id: "toothmask", name: "치흔지수" },
    ];

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
            this.dataset_id = "yd5m3OpaRuAbm2dfRyh7ks2LT4e5vqsZ";
        }
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        this.labels = data.label;
        this.datas = data.value;

        await this.service.render();
    }

    private async loadGraph(mode) {
        if (mode) {
            this.mode = mode;
        }

        if (this.myChart) {
            this.myChart.clear();
            this.myChart.destroy();
        }

        let data_pie;
        if (this.mode == "lightred" || this.mode == "coated") {
            this.colors = ['#3B29EC', '#8F86F4', '#E8E5FD'];
            if (this.mode == "lightred") {
                data_pie = this.datas.lightred;
                this.labels = ['담홍지수 - 담백설', '담홍지수 - 담홍설', '담홍지수 - 홍설'];
            }
            else {
                data_pie = this.datas.coated;
                this.labels = ['설태지수 - 박태', '설태지수 - 정상', '설태지수 - 후태'];
            }
        }

        else {
            this.colors = ['#E81841', '#FAD1D9'];
            if (this.mode == "bluepurple") {
                data_pie = this.datas.bluepurple;
                this.labels = ['청자지수 - 정상', '청자지수 - 청자설'];
            }
            else {
                data_pie = this.datas.toothmask;
                this.labels = ['치흔지수 - 정상', '치흔지수 - 강함'];
            }
        }

        const total = data_pie.reduce((a, b) => parseInt(a) + parseInt(b), 0);
        const data = {
            labels: this.labels,
            datasets: [{
                data: data_pie,
                backgroundColor: this.colors,
                borderColor: this.colors,
                borderWidth: 1,
                pointStyle: 'circle'
            }]
        };

        const config = {
            type: 'pie',
            data: data,
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true
                        }
                    },
                    title: {
                        display: true,
                        text: 'Total - ' + total,
                        align: 'end',
                        font: { size: '18px' }
                    },
                    datalabels: {
                        color: 'white',
                        font: {
                            weight: 'bold',
                            size: '14px'
                        },
                        padding: 6,
                        formatter: (value) => {
                            const percentage = (value / total) * 100;
                            return percentage.toFixed(1) + '%';
                        },
                    }
                }
            }
        };

        const ctx = document.getElementById('widget-tongue').getContext('2d');
        ctx.canvas.height = 400;
        ctx.canvas.width = 875;
        this.myChart = new Chart(ctx, config);

        await this.service.render();
    }
}