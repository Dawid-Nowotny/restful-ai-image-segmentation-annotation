import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { TabDirective, TabsModule } from 'ngx-bootstrap/tabs';
import Chart from 'chart.js/auto';
import { ServerService } from '../services/server.service';
import ChartDataLabels from 'chartjs-plugin-datalabels';

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
	chart!: Chart;

	topTagsArray: TopTagData[] = [];
	popularTagsByMonthArray: PopularTagsByMonthData[] = [];

	constructor(private serverService: ServerService) {
		Chart.register(ChartDataLabels);
	}

	ngAfterViewInit(): void {
		this.createTopTagsChart();
	}

	handleTabChange(tab: TabDirective) {
		switch(tab.id){
			case 'tab1': this.createTopTagsChart(); break;
			case 'tab2': this.createPopularTagsByMonthChart(); break;
		}
		// this.createPopularTagsByMonthChart();
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
				let labels = response.map((tag: any, index: number) => [tag.month, `tag: ${tag.top_tag.tag}`]);
				let data = response.map((tag: any) => tag.top_tag.count);
				let dataLabels = response.map((tag: any) => tag.top_tag.tag);
				this.createChart(this.popularTagsByMonthChartCanvas, "Popularne tagi w poszczególnych miesiącach", labels, data);
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
		if(this.chart){
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
