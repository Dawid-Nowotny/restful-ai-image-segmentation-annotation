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
    private restUrl = 'http://localhost:9000/api';
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

    postLogout(): Observable<any> {
        const url = `${this.restUrl}/user/logout`;
        return this.http.post(url, {});
    }

    getLoggedUserCredentials(): Observable<any> {
        const url = `${this.restUrl}/user/me`;

        return this.http.get(url);
    }

    /** GET PROFILE INFO */
    getProfileInfo(username: string): Observable<any> {
        const url = `${this.restUrl}/user/get-profile-info/${username}`;
        return this.http.get(url);
    }

    updateUser(userDataUpdate: any): Observable<any> {
        const url = `${this.restUrl}/user/update-user`;
        return this.http.patch(url, userDataUpdate);
    }

    generateQrCode(): Observable<Blob> {
        const url = `${this.restUrl}/user/generate-qr`;

        return this.http.post(url, null, { responseType: 'blob' });
    }

    verifyTOTP(data: any): Observable<any> {
        const url = `${this.restUrl}/user/verify-code`;

        const body = {
            token: data.verificationCode
        }

        return this.http.post(url, body);
    }

    disableTOTP(password: string): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/user/disable-totp`;
        const body = { password: password };

        return this.http.put(url, body, { headers });
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

    getImage(id: number) {
        const url = `${this.restUrl}/images/get-image/${id}`;
        return this.http.get(url, { responseType: "blob" });
    }

    getUserImages(username: string, startId: number, endId: number) {
        const url = `${this.restUrl}/images/get-user-images/${username}/images/${startId}/${endId}`;
        return this.http.get(url, { responseType: 'arraybuffer' });
    }

    getImagesAsZip(startId: number, endId: number) {
        const url = `${this.restUrl}/images/get-images/${startId}/${endId}`;
        return this.http.get(url, { responseType: "arraybuffer" });
    }

    getFilteredImagesAsZip(
        startId: number,
        endId: number,
        thresholdFrom: number,
        thresholdTo: number,
        tags: string[],
        classes: string[]
    ) {

        console.log(thresholdFrom, thresholdTo);

        let thresholdParam = `threshold_range=${thresholdFrom}%2C${thresholdTo}`;
        let tagsParam = tags.length > 0 ? `tags=${tags}` : "";
        let classesParam = classes.length > 0 ? `classes=${classes}` : "";

        const url = `${this.restUrl}/images/get-filtered-images/%7Bfilters%7D/${startId}/${endId}?${thresholdParam}&${tagsParam}&${classesParam}`;
        return this.http.get(url, { responseType: "arraybuffer" });
    }

    getSegmentedImage(image_id: number): Observable<Blob> {
        const url = `${this.restUrl}/images/get-segmented-image/${image_id}`;
        return this.http.get(url, { responseType: 'blob' })
    }

    getImageAuthor(image_id: number) {
        const url = `${this.restUrl}/images/get-image-uploader/${image_id}`;
        return this.http.get(url)
    }

    getSuperTagsAuthor(image_id: number) {
        const url = `${this.restUrl}/images/get-image-super-tag-author/${image_id}`;
        return this.http.get(url)
    }

    getImageDetections(image_id: number) {
        const url = `${this.restUrl}/images/get-image-detections/${image_id}`;
        return this.http.get(url)
    }

    getImageSuggestedAnnotations(imageId: number): Observable<any> {
        const url = `${this.restUrl}/images/suggest-annotations/${imageId}`;
        return this.http.get(url);
    }

    getImageSuperTags(imageId: number): Observable<any> {
        const url = `${this.restUrl}/images/get-image-super-tags/${imageId}`;
        return this.http.get(url);
    }

    getImageComments(imageId: number): Observable<any> {
        const url = `${this.restUrl}/images/get-image-comments/${imageId}`;
        return this.http.get(url);
    }

    getTopTags(limit: number): Observable<any> {
        const url = `${this.restUrl}/statistics/top-tags/${limit}`;
        return this.http.get(url);
    }

    getPopularTagsByMonth(): Observable<any> {
        const url = `${this.restUrl}/statistics/popular-tags-by-month`;
        return this.http.get(url);
    }

    getTopClasses(limit: number): Observable<any> {
        const url = `${this.restUrl}/statistics/top-classes/${limit}`;
        return this.http.get(url);
    }

    getPopularClassesByMonth(): Observable<any> {
        const url = `${this.restUrl}/statistics/popular-classes-by-month`;
        return this.http.get(url);
    }

    getTopUploaders(limit: number): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/statistics/top-uploaders/${limit}`;
        return this.http.get(url, { headers });
    }

    getTopCommenters(limit: number): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/statistics/top-commenters/${limit}`;
        return this.http.get(url, { headers });
    }

    getTopModerators(limit: number): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/statistics/moderated-images/${limit}`;
        return this.http.get(url, { headers });
    }

    addSuperTagToImage(imageId: number, tagsArray: string[]): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/admin/add-super-tag/`;

        const tagsInRequest = tagsArray.map(tag => {
            return {
                tag: tag
            }
        })

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

    addCommentToImage(imageId: number, tagsArray: string[]) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/images/add-comment-to-image/`;

        const tagsInRequest = tagsArray.map(tag => {
            return {
                tag: tag
            }
        })

        const body = {
            request: {
                image_id: imageId,
            },
            comment_data: {
                super_tag: false,
                tags: tagsInRequest
            }
        }
        
        return this.http.post(url, body, { headers });
    }

    getImagesNumber() {
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

    assignModeratorToImage(imageId: number, username: string) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        const url = `${this.restUrl}/admin/assign-moderator/${imageId}/${username}`;
        return this.http.put(url, {}, { headers });
    }

    assignModeratorRole(username: string): Observable<any> {
        const url = `${this.restUrl}/admin/make-moderator/${username}`;
        return this.http.put(url, {});
    }

    removeModeratorRole(username: string): Observable<any> {
        const url = `${this.restUrl}/admin/remove-moderator-role/${username}`;
        return this.http.put(url, {});

    }
}