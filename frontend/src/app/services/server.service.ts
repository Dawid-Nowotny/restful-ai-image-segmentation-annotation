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

    /** GET PROFILE INFO */
    getProfileInfo(username: string): Observable<any> {
        const url = `${this.restUrl}/user/get-profile-info/${username}`;
        return this.http.get(url);
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
        const url = `${this.restUrl}/images/get-image/${id}`;
        return this.http.get(url, {responseType: "blob"});
    }

    getImagesAsZip(startId: number, endId: number) {
        const url = `${this.restUrl}/images/get-images/${startId}/${endId}`;
        return this.http.get(url, { responseType: "arraybuffer" });
    }

    getSegmentedImage(image_id: number): Observable<Blob> {
        const url = `${this.restUrl}/images/get-segmented-image/${image_id}`;
        return this.http.get(url, { responseType: 'blob' })
    }

    getImageAndSuperTagsAuthors(image_id: number) {
        const url = `${this.restUrl}/images/get-image-data/${image_id}`;
        return this.http.get(url)
    }

    getImageSuperTags(imageId: number): Observable<any>{
        const url = `${this.restUrl}/images/get-image-super-tags/${imageId}`;
        return this.http.get(url);
    }

    addSuperTagToImage(accessToken: string, imageId: number, tagsArray: string[]): Observable<any> {
        const headers = new HttpHeaders({
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/admin/add-super-tag/`;

        const tagsInRequest = tagsArray.map(tag => {
            return {
                tag: tag
            }
        })
        console.log(tagsInRequest);

        const body = {
            request: {
                image_id: imageId,
            },
            comment_data: {
                super_tag: true,
                tags: tagsInRequest
            }
        }

        return this.http.post(url, body, { headers }); 
    }

    getImagesNumber(){
        const url = `${this.restUrl}/images/get-images-number`;
        return this.http.get(url);
    }

    getModerators(): Observable<any> {
        const url = `${this.restUrl}/admin/moderators-list`;
        return this.http.get(url);
    }

    getUsers(): Observable<any> {
        const url = `${this.restUrl}/admin/users-list`;
        return this.http.get(url);
    }

    getImageModerator(imageId: number): Observable<any> {
        const url = `${this.restUrl}/images/get-image-moderator/${imageId}`;
        return this.http.get(url);
        
    }

    assignModeratorToImage(accessToken: string, imageId: number, username: string) {
        const headers = new HttpHeaders({
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/admin/assign-moderator/${imageId}/${username}`;
        return this.http.put(url, {}, { headers });
    }
}
