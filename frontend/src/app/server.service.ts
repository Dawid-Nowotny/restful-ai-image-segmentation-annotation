import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})

export class ServerService {
  private restUrl = 'http://127.0.0.1:8000';
  constructor(private http: HttpClient) { }

   /** POST LOGIN */
   postLogin(data: any): Observable<any> {
    const url = `${this.restUrl}/user/login`;
    return this.http.post(url, data, httpOptions);
  }

  /** POST REGISTER */
  postRegister(data: any): Observable<any> {
    const url = `${this.restUrl}/user/register`;
    return this.http.post(url, data, httpOptions);
  }
}
