import { AfterViewInit, Component, ElementRef, ViewChild, viewChild } from '@angular/core';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { TabDirective, TabsModule } from 'ngx-bootstrap/tabs';
import { ServerService } from '../services/server.service';
import { LoggedUserService } from '../services/logged-user.service';
import { CommonModule } from '@angular/common';
import { ChartService } from '../services/chart.service';

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

type TopCommentersData = {
	username: string,
	comment_count: number,
}

type TopModeratorsData = {
	username: string,
	moderated_count: number,
}

@Component({
	selector: 'app-statistics-panel',
	standalone: true,
	imports: [CommonModule, TabsModule],
	templateUrl: './statistics-panel.component.html',
	styleUrl: './statistics-panel.component.css'
})
export class StatisticsPanelComponent implements AfterViewInit {

	@ViewChild('topTagsChart') topTagsChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('popularTagsByMonthChart') popularTagsByMonthChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topClassesChart') topClassesChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('popularClassesByMonthChart') popularClassesByMonthChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topUploadersChart') topUploadersChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topCommentersChart') topCommentersChartCanvas!: ElementRef<HTMLCanvasElement>;
	@ViewChild('topModeratorsChart') topModeratorsChartCanvas!: ElementRef<HTMLCanvasElement>;

	chart!: Chart;

	constructor(
		public loggedUserService: LoggedUserService,
		private chartService: ChartService
	) {
		Chart.register(ChartDataLabels);
	}

	ngAfterViewInit(): void {
		this.chartService.createTopTagsChart(this.topTagsChartCanvas);
	}

	handleTabChange(tab: TabDirective) {
		switch (tab.id) {
			case 'tab1':
				this.chartService.createTopTagsChart(this.topTagsChartCanvas); break;
			case 'tab2':
				this.chartService.createPopularTagsByMonthChart(this.popularTagsByMonthChartCanvas); break;
			case 'tab3':
				this.chartService.createTopClassesChart(this.topClassesChartCanvas); break;
			case 'tab4':
				this.chartService.createPopularClassesByMonthChart(this.popularClassesByMonthChartCanvas); break;
			case 'tab5':
				this.chartService.createTopUploadersChart(this.topUploadersChartCanvas); break;
			case 'tab6':
				this.chartService.createTopCommentersChart(this.topCommentersChartCanvas); break;
			case 'tab7':
				this.chartService.createTopModeratorsChart(this.topModeratorsChartCanvas); break;
		}
	}

}
