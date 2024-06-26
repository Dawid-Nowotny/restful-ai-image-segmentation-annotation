import { ElementRef, Injectable } from '@angular/core';
import { Chart } from 'chart.js';
import { ServerService } from './server.service';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { LoggedUserService } from './logged-user.service';

type TopClassesData = {
    class_name: string,
    count: number,
}

type PopularClassesByMonthData = {
    year: number,
    month: string,
    top_classes: {
        class_name: string,
        count: number,
    }
}

type TopUploadersData = {
    username: string,
    upload_count: number,
}

type TopCommentersData = {
    username: string,
    comment_count: number,
}

type TopModeratorsData = {
    username: string,
    moderated_count: number,
}

@Injectable({
    providedIn: 'root'
})
export class ChartService {

    chart!: Chart;

    constructor(private serverService: ServerService) {
        Chart.register(ChartDataLabels);
    }

    createTopTagsChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
        this.serverService.getTopTags(10).subscribe({
            next: (response: any) => {
                let labels = response.map((tag: any) => tag.tag);
                let data = response.map((tag: any) => tag.count);
                this.createChart(chartElementRef, "Top 10 tagów", labels, data);
            },
            error: (error: Error) => {
                console.log(error);
            }
        })
    }

    createPopularTagsByMonthChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
        this.serverService.getPopularTagsByMonth().subscribe({
            next: (response: any) => {
                let labels = response.map((tag: any) => [tag.month, `tag: ${tag.top_tag.tag}`]);
                let data = response.map((tag: any) => tag.top_tag.count);
                this.createChart(chartElementRef, "Popularne tagi w poszczególnych miesiącach", labels, data);
            },
            error: (error: Error) => {
                console.log(error);
            }
        })
    }

    createTopClassesChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
        this.serverService.getTopClasses(10).subscribe({
            next: (response: any) => {
                let labels = response.map((imageClass: TopClassesData) => imageClass.class_name);
                let data = response.map((imageClass: TopClassesData) => imageClass.count);
                this.createChart(chartElementRef, "Top 10 klas", labels, data);
            },
            error: (error: Error) => {
                console.log(error);
            }
        })
    }

    createPopularClassesByMonthChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
        this.serverService.getPopularClassesByMonth().subscribe({
            next: (response: PopularClassesByMonthData[]) => {
                let labels: any = response.map(imageClass => [imageClass.month, `klasa: ${imageClass.top_classes.class_name}`]);
                let data = response.map((imageClass: PopularClassesByMonthData) => imageClass.top_classes.count);
                this.createChart(
                    chartElementRef,
                    "Popularne klasy w poszczególnych miesiącach",
                    labels,
                    data
                );
            },
            error: (error: Error) => {
                console.log(error);
            }
        })
    }

    createTopUploadersChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
        this.serverService.getTopUploaders(10).subscribe({
            next: (response: TopUploadersData[]) => {
                let labels = response.map((uploader: TopUploadersData) => uploader.username);
                let data = response.map((uploader: TopUploadersData) => uploader.upload_count);
                this.createChart(chartElementRef, "Top 10 uploaderów", labels, data);
            },
            error: (error: Error) => {
                console.log(error);
            }
        })
    }

    createTopCommentersChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
		this.serverService.getTopCommenters(10).subscribe({
			next: (response: TopCommentersData[]) => {
				let labels = response.map((uploader: TopCommentersData) => uploader.username);
				let data = response.map((uploader: TopCommentersData) => uploader.comment_count);
				this.createChart(chartElementRef, "Top 10 komentujących", labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

	createTopModeratorsChart(chartElementRef: ElementRef<HTMLCanvasElement>) {
		this.serverService.getTopModerators(10).subscribe({
			next: (response: TopModeratorsData[]) => {
				let labels = response.map((moderator: TopModeratorsData) => moderator.username);
				let data = response.map((moderator: TopModeratorsData) => moderator.moderated_count);
				this.createChart(chartElementRef, "Top 10 moderatorów", labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

    createChart(
        chartElementRef: ElementRef<HTMLCanvasElement>,
        title: string,
        labels: string[],
        data: number[],
    ) {
        if (this.chart) {
            this.chart.destroy();
        }

        this.chart = new Chart(chartElementRef.nativeElement, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: title,
                        data: data,
                        backgroundColor: 'rgba(46, 204, 113, 0.2)',
                        borderColor: 'rgba(46, 204, 113, 1)',
                        borderWidth: 2,
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            font: {
                                size: 16
                            }
                        },
                    },
                    y: {
                        ticks: {
                            font: {
                                size: 16
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 20
                            },
                        },
                    },
                }
            }
        });
    }
}
