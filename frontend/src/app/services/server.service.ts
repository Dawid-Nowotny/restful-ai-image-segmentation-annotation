import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
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

        const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
        const url = `${this.restUrl}/user/login`;
        const body = new HttpParams()
            .set('username', data.username)
            .set('password', data.password);

        return this.http.post(url, body, { headers });
    }

    getLoggedUserCredentials(JWTToken: string): Observable<any> {
        const headers = new HttpHeaders({
            'Authorization': `Bearer ${JWTToken}`,
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/user/me`;

        return this.http.get(url, { headers });
    }

    verifyTOTP(data: any): Observable<any> {
        const headers = new HttpHeaders({
            'Authorization': `Bearer ${data.accessToken}`,
            'Content-Type': 'application/json'
        });
        const queryParam = `token=${data.verificationCode}`
        const url = `${this.restUrl}/user/verify-code?${queryParam}`;

        return this.http.post(url, {}, { headers });
    }
    /** POST REGISTER */
    postRegister(data: any): Observable<any> {
        const url = `${this.restUrl}/user/register`;
        return this.http.post(url, data, httpOptions);
    }

    postImage(data: any): Observable<any> {
        const url = `${this.restUrl}/images/upload`;
        return this.http.post(url, data);
    }

    getImage(id: number){
        const url = `${this.restUrl}/images/get_image/${id}`;
        return this.http.get(url, {responseType: "blob"});
    }

    getImagesAsZip(startId: number, endId: number) {
        const url = `${this.restUrl}/images/get_images/${startId}/${endId}`;
        return this.http.get(url, { responseType: "arraybuffer" });
    }

    getModerators(): Observable<any> {
        const url = `${this.restUrl}/admin/moderators-list`;
        return this.http.get(url);
    }
}
