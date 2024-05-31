import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { TabDirective, TabsModule } from 'ngx-bootstrap/tabs';
import { ServerService } from '../services/server.service';
import { LoggedUserService } from '../services/logged-user.service';

type TopTagData = {
	tag: string,
	count: number,
}

type PopularTagsByMonthData = {
	year: number,
	month: string,
	top_tag: {
		tag: string,
		count: number
	}
}

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

@Component({
	selector: 'app-statistics-panel',
	standalone: true,
	imports: [TabsModule],
	templateUrl: './statistics-panel.component.html',
	styleUrl: './statistics-panel.component.css'
})
export class StatisticsPanelComponent implements AfterViewInit {

	@ViewChild('topTagsChart') topTagsChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('popularTagsByMonthChart') popularTagsByMonthChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topClassesChart') topClassesChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('popularClassesByMonthChart') popularClassesByMonthChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topUploadersChart') topUploadersChartCanvas!: ElementRef<HTMLCanvasElement>;

	chart!: Chart;

	constructor(private serverService: ServerService, private loggedUserService: LoggedUserService) {
		Chart.register(ChartDataLabels);
	}

	ngAfterViewInit(): void {
		this.createTopTagsChart();
	}

	handleTabChange(tab: TabDirective) {
		switch (tab.id) {
			case 'tab1': this.createTopTagsChart(); break;
			case 'tab2': this.createPopularTagsByMonthChart(); break;
			case 'tab3': this.createTopClassesChart(); break;
			case 'tab4': this.createPopularClassesByMonthChart(); break;
			case 'tab5': this.createTopUploadersChart(); break;
		}
	}

	createTopTagsChart() {
		this.serverService.getTopTags(10).subscribe({
			next: (response: any) => {
				let labels = response.map((tag: any) => tag.tag);
				let data = response.map((tag: any) => tag.count);
				this.createChart(this.topTagsChartCanvas, "Top 10 tagów", labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

	createPopularTagsByMonthChart() {
		this.serverService.getPopularTagsByMonth().subscribe({
			next: (response: any) => {
				let labels = response.map((tag: any) => [tag.month, `tag: ${tag.top_tag.tag}`]);
				let data = response.map((tag: any) => tag.top_tag.count);
				this.createChart(this.popularTagsByMonthChartCanvas, "Popularne tagi w poszczególnych miesiącach", labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

	createTopClassesChart() {
		this.serverService.getTopClasses(10).subscribe({
			next: (response: any) => {
				let labels = response.map((imageClass: TopClassesData) => imageClass.class_name);
				let data = response.map((imageClass: TopClassesData) => imageClass.count);
				this.createChart(this.topClassesChartCanvas, "Top 10 klas", labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

	createPopularClassesByMonthChart() {
		this.serverService.getPopularClassesByMonth().subscribe({
			next: (response: PopularClassesByMonthData[]) => {
				let labels: any = response.map(imageClass => [imageClass.month, `klasa: ${imageClass.top_classes.class_name}`]);
				let data = response.map((imageClass: PopularClassesByMonthData) => imageClass.top_classes.count);
				this.createChart(
					this.popularClassesByMonthChartCanvas,
					"Popularne klasy w poszczególnych miesiącach",
					labels,
					data
				);
			},
		})
	}

	createTopUploadersChart() {
		this.serverService.getTopUploaders(this.loggedUserService.getAccessToken(), 10).subscribe({
			next: (response: TopUploadersData[]) => {
				let labels = response.map((uploader: TopUploadersData) => uploader.username);
				let data = response.map((uploader: TopUploadersData) => uploader.upload_count);
				this.createChart(this.topUploadersChartCanvas, "Top 10 uploaderów", labels, data);
			},

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
