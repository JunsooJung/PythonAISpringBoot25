package org.mbc.controller;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserter;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@RestController // 비동기 방식 컨트롤러
public class RestReqController {

    @Autowired // NEW 대신
    private WebClient webClient;

    @PostMapping("/java_service")
    public String serviceRequest(MultipartFile file, String message){
        MultipartBodyBuilder bodyBuilder = new  MultipartBodyBuilder();
        // 멀티 파트 폼 데이터 구성
        bodyBuilder.part("message", message);           // 폼데이터 메세지
        bodyBuilder.part("file", file.getResource());   // 폼 데이터 파일
        String result = webClient.post().uri("/detect")
                // POST 방식 요청, /detect
                .contentType(MediaType.MULTIPART_FORM_DATA) // 파일 전송
                .body(BodyInserters.fromMultipartData(bodyBuilder.build()))
                // 폼 데이터 요청 본문 설정
                .retrieve() // 실행 및 응답받기
                .bodyToMono(String.class)
                //본문 -> string 전환
                .block(); //비동기 처리 블록 결과반환

        return result;
        // 1. 자바 rest 컨트롤러로 텍스트, 이미지 비동기 방식 전송
        // 2. AI 서버에서 이미지 받아 객체 탐지 수행
        // 3. AI서버에서 base64 인코딩
        // 4. rest 컨트롤러에서 비동기 방식 텍스트 이미지 변환
        // 5. 비동기 요청한 뷰 페이지에서 결과 출력


    }


}
