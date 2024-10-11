import { useState, useEffect } from "react";
import axios from "axios";
import "./results.css";

interface ImageData {
  //{ img1: string, img2: string }
  img1: string;
  img2: string;
}
interface ResultData {
  library_value: number[];
  without_library_value: number[];
}

function Results() {
  const [images, setImages] = useState<ImageData[]>([]);
  const [values, setValues] = useState<ResultData[]>([]);

  useEffect(() => {
    //bileşen yüklendiğinde içine yazılan kodu bir kez çalıştır.

    axios
      .get("http://localhost:5000/get_image")
      .then((response) => {
        console.log(response.data[0]); //img1 : "/static/images/data_1_library.png"
        const all_data = {
          img1: response.data[0].img1, // img1 verisini al
          img2: response.data[1].img2, // img2 verisini al
        };
        setImages([all_data]);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });

    axios
      .get("http://localhost:5000/get_results")
      .then((response) => {
        console.log(response.data);
        const all_values = {
          library_value: response.data["value1"],
          without_library_value: response.data["value2"],
        };
        setValues([all_values]);
        console.log(all_values);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  function download_file() {
    axios
      .get("http://localhost:5000/download_csv", { responseType: "blob" }) // blob veri tipi binary
      .then((response) => {
        console.log(response);
        const url = window.URL.createObjectURL(new Blob([response.data])); //tarayıcıda indirilebilir  dosya URLsi
        const link = document.createElement("a"); //tarayıcıya bağlantı  olıuşturur
        link.href = url;
        link.setAttribute("download", "result.csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
  }

  return (
    <div className="elements">
      <div className="container-fluid mt-4">
        <h1 className=" text-center mb-4 title">Results</h1>
        <div className="row justify-content-between">
          {images.map((item, index) => (
            <>
              <div className="col-4 box ms-3" key={index}>
                <img
                  src={`http://localhost:5000${item.img1}`} // Resmin tam yolu
                  className="img-fluid"
                  alt="Scikit- Learn Kütüphanesi Çıktısı" // Resim için alt text
                />
              </div>

              <div className="col-4 box" key={index}>
                <img
                  src={`http://localhost:5000${item.img2}`} // Resmin tam yolu
                  className="img-fluid "
                  alt={"Kütüphane Kullanılmamış Versiyon Çıktısı"} // Resim için alt text
                />
              </div>
            </>
          ))}

          <div className="col-3 box me-3 result">
            <div className=" row-4 download-bar">
              <div className="input-group mt-2">
                <input
                  type="text"
                  className="form-control text-align center"
                  value="result.csv"
                  readOnly
                />
                <div className="input-group-append" onClick={download_file}>
                  <a className="btn btn-outline-secondary" download>
                    Download
                  </a>
                </div>
              </div>
            </div>

            <div className="row-6 result-row mt-5">
              <p className="table-caption">Result of Algorithm with Library</p>
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col"></th>
                    <th scope="col">Result</th>
                  </tr>
                </thead>
                {values.map((item, index) => (
                  <tbody>
                    <tr>
                      <th scope="row">Execution time:</th>
                      <td>{item.library_value[0]}</td>
                    </tr>
                    <tr>
                      <th scope="row">Optimum Cluster Number:</th>
                      <td>{item.library_value[1]}</td>
                    </tr>
                    <tr>
                      <th scope="row">Silhoutte Score</th>
                      <td>{item.library_value[2]}</td>
                    </tr>
                  </tbody>
                ))}
              </table>
            </div>

            <div className="row-6 result-row mt-5">
              <p className="table-caption">
                Result of Algorithm without Library
              </p>
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col"></th>
                    <th scope="col">Result</th>
                  </tr>
                </thead>
                {values.map((item, index) => (
                  <tbody>
                    <tr>
                      <th scope="row">Execution time:</th>
                      <td>{item.without_library_value[0]}</td>
                    </tr>
                    <tr>
                      <th scope="row">Optimum Cluster Number:</th>
                      <td>{item.without_library_value[1]}</td>
                    </tr>
                    <tr>
                      <th scope="row">Silhoutte Score</th>
                      <td>{item.without_library_value[2]}</td>
                    </tr>
                  </tbody>
                ))}
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Results;
