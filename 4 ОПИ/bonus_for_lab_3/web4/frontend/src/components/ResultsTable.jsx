import React from 'react';

const ResultsTable = ({ points }) => {

  const formatExecTime = (ns) => {
    if (ns === undefined || ns === null) return '—';
    if (ns < 1000000) {
      return `${(ns / 1000).toFixed(0)} мкс`;
    }
    return `${(ns / 1000000).toFixed(2)} мс`;
  };

  return (
      <div className="table-wrapper">
        <table className="results-table">
          <thead>
          <tr>
            <th>ID</th>
            <th>X</th>
            <th>Y</th>
            <th>R</th>
            <th>Результат</th>
            <th>Время скрипта</th>
            <th>Дата и время</th>
          </tr>
          </thead>
          <tbody>
          {points.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{Number(p.x).toFixed(3)}</td>
                <td>{Number(p.y).toFixed(3)}</td>
                <td>{p.r}</td>
                <td className={`results-table-cell ${p.hit ? 'hit' : 'miss'}`}>
                  {p.hit ? 'Попал' : 'Промах'}
                </td>
                <td>{formatExecTime(p.executionTimeNs)}</td>
                <td>
                  {p.createdAt
                      ? new Date(p.createdAt).toLocaleTimeString('ru-RU', { hour12: false })
                      : '—'}
                </td>
              </tr>
          ))}
          </tbody>
        </table>
      </div>
  );
};

export default ResultsTable;