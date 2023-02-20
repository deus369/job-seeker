A quick and dirty app, automates/assists job seeking.

    - Saves encrypted password
    - Scans job search terms
    - Saves job application states
    - Applies for jobs with resume and cover letter

<div style="display: flex; justify-content: center; flex-wrap: wrap;">
  <div class="gallery-item">
    <a href="screenshots/Screenshot_2023-02-20_19-08-21.png" target="_blank">
      <img src="screenshots/Screenshot_2023-02-20_19-08-21.png">
    </a>
  </div>
  <div class="gallery-item">
    <a href="screenshots/Screenshot_2023-02-20_19-08-51.png" target="_blank">
      <img src="screenshots/Screenshot_2023-02-20_19-08-51.png">
    </a>
  </div>
  <div class="gallery-item">
    <a href="screenshots/Screenshot_2023-02-20_19-09-22.png" target="_blank">
      <img src="screenshots/Screenshot_2023-02-20_19-09-22.png">
    </a>
  </div>
</div>

<style>
    .gallery-item {
        flex: 1;
        margin: 10px;
        position: relative;
    }

    .gallery-item img {
        max-width: 100%;
        height: auto;
    }

    .gallery-item a:before {
        content: "";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-color: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.3s;
    }

    .gallery-item a:hover:before {
        opacity: 1;
    }

    .gallery-item a:after {
        content: "View Larger";
        display: block;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 18px;
        color: #fff;
        text-align: center;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .gallery-item a:hover:after {
        opacity: 1;
    }
</style>
