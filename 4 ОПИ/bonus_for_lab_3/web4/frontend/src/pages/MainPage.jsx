import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'; 
import { fetchPoints, addPoint, clearPoints, clearPointsError } from '../store/pointsSlice';
import Graph from '../components/Graph';
import ResultsTable from '../components/ResultsTable';
import { validateY, normalizeInput, handleInputKeyDown } from '../utils/validation';
import './Pages.css';

const MainPage = () => {
  const dispatch = useDispatch();

  const { items: points, error: backendError } = useSelector((state) => state.points);

  const [x, setX] = useState(0);
  const [y, setY] = useState('');
  const [r, setR] = useState(1);
  const [errorMsg, setErrorMsg] = useState('');

  const xOptions = [-5, -4, -3, -2, -1, 0, 1, 2, 3];
  const rOptions = [-5, -4, -3, -2, -1, 0, 1, 2, 3];

  useEffect(() => {
    dispatch(fetchPoints());
  }, [dispatch]);

  useEffect(() => {
    if (backendError) {
      setErrorMsg(backendError);

      dispatch(clearPointsError());
    }
  }, [backendError]);

  const handleYChange = (e) => {
    const sanitizedValue = normalizeInput(e.target.value);
    setY(sanitizedValue);
    if (errorMsg) {
      setErrorMsg('');
      dispatch(clearPointsError());
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationError = validateY(y);
    if (validationError) {
      setErrorMsg(validationError);
      return;
    }
    setErrorMsg('');
    dispatch(clearPointsError());
    dispatch(addPoint({ x: Number(x), y: parseFloat(y), r: Number(r) }));
  };

  const handleGraphClick = (xGraph, yGraph) => {
    setErrorMsg('');
    dispatch(clearPointsError());

    dispatch(addPoint({
      x: xGraph.toFixed(4),
      y: yGraph.toFixed(4),
      r: Number(r)
    }));
  };

  const handleClear = () => {
    dispatch(clearPoints());
    setErrorMsg('');
    dispatch(clearPointsError());
  }

  const recentPoints = points; //.slice(0, 10);

  return (
      <div className="main-page-centered">
        <div className="graph-section">
          <Graph r={Number(r)} points={recentPoints} onGraphClick={handleGraphClick} />
        </div>

        <form className="coord-form-new" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="input-group">
              <label>X:</label>
              <select value={x} onChange={(e) => setX(e.target.value)}>
                {xOptions.map(val => (
                    <option key={val} value={val}>{val}</option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label>Y:</label>
              <input
                  type="text"
                  value={y}
                  onChange={handleYChange}
                  onKeyDown={handleInputKeyDown}
                  placeholder="(-3 ... 5)"
                  className="input-y"
                  autoComplete="off"
              />
            </div>

            <div className="input-group">
              <label>R:</label>
              <div className="radio-group-container">
                {rOptions.map(val => (
                    <label key={val} className="radio-label">
                      <input
                          type="radio"
                          value={val}
                          checked={Number(r) === val}
                          onChange={(e) => setR(e.target.value)}
                      />
                      {val}
                    </label>
                ))}
              </div>
            </div>
          </div>

          {errorMsg && <div className="error-msg-center">{errorMsg}</div>}

          <div className="form-actions">
            <button type="submit" className="btn-submit">Проверить</button>
            <button type="button" className="btn-clear" onClick={handleClear}>Очистить</button>
          </div>
        </form>

        <div className="table-section">
          <ResultsTable points={recentPoints} />
        </div>
      </div>
  );
};

export default MainPage;