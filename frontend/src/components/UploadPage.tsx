import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./upload.css";

function Upload() {
  const [file, setFile] = useState<File | null>(null); // başlangıçta null ama değeri ya null olacak ya da File olacak anlamında // bileşenin (component) durumunu yönetilir.

  const [kValue, setKValue] = useState("");
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); //formu yeniden yüklemeyi durdurur.
    if (!file || !kValue) {
      setError("Dosya veya K değeri eksik.");
      return;
    }

    const fd = new FormData();
    fd.append("file", file);
    fd.append("cluster_num", kValue);

    axios
      .post("http://127.0.0.1:5000", fd, {
        headers: {
          "custom-type": "value", //"Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        setMsg("Yükleme Başarılı");
        navigate("/result");
      })
      .catch((err) => {
        setMsg("Yükleme Başarısız");
        console.log(err);
      });
  }

  return (
    <div className="container text-center">
      <form className="row justify-content-center" onSubmit={handleUpload}>
        <div className="row mb-5">
          <h1>K-Means Clustering Algorithm</h1>
        </div>
        {error && <div className="alert alert-danger">{error}</div>}

        <div className="row mb-3 mt-3">
          <div className="col-sm-6">
            <label htmlFor="formFile" className="form-label">
              Upload the Dataset :
            </label>
          </div>
          <div className="col-sm-3">
            <input
              onChange={(e) =>
                setFile(
                  e.target.files && e.target.files[0] ? e.target.files[0] : null
                )
              } //Tarayıcıda gerçekleşen bir olayın bilgisini tutar
              className="form-control"
              type="file"
              accept=".csv"
              id="formFile"
            />
          </div>
        </div>

        <div className="row mb-3">
          <div className="col-sm-6">
            <label htmlFor="k-value" className="form-label">
              Enter the Maximum Number of Clusters to Be Tested:
            </label>
          </div>
          <div className="col-sm-3">
            <input
              className="form-control"
              id="k-value"
              type="number"
              min="2"
              value={kValue}
              onChange={(e) => setKValue(e.target.value)}
            />
          </div>
        </div>

        <div className="row mb-3 mt-5">
          <div className="col-sm-4"></div>
          <div className="col-sm-3">
            <button type="submit" className="btn btn-success">
              View Results
            </button>
            <span>{msg}</span>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Upload;
