import { useState, useEffect } from 'react'
import api from '../services/api'

function ModelMetrics() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await api.getHealth()
        setHealth(data)
      } catch (err) {
        console.error('Error fetching health:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchHealth()
  }, [])

  // Métricas reales de DistilBERT (del README)
  const distilbertMetrics = {
    test_accuracy: 88.33,
    validation_accuracy: 91.64,
    f1_score: 83.9,
    precision: 84.6,
    recall: 83.3,
    overfitting: 3.3,
    parameters: '66M'
  }

  const logisticMetrics = {
    test_accuracy: 52.5,
    f1_score: 65.7,
    precision: 49.2,
    recall_toxic: 98.9,
    overfitting: 23.1
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-purple-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-900 to-blue-900 rounded-xl p-8 border-2 border-purple-600">
        <h1 className="text-4xl font-bold text-white mb-4">📊 Métricas del Modelo</h1>
        <p className="text-gray-300">
          Comparación detallada del rendimiento entre DistilBERT y Logistic Regression
        </p>
      </div>

      {/* Estado del Sistema */}
      {health && (
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <span className="text-green-400">●</span> Estado del Sistema
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Estado General</p>
              <p className="text-white font-bold text-xl capitalize">{health.status}</p>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Logistic Regression</p>
              <p className={`font-bold text-xl ${health.models.logistic_regression.loaded ? 'text-green-400' : 'text-red-400'}`}>
                {health.models.logistic_regression.loaded ? '✅ Cargado' : '❌ No disponible'}
              </p>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <p className="text-gray-400 text-sm">DistilBERT</p>
              <p className={`font-bold text-xl ${health.models.distilbert.loaded ? 'text-green-400' : 'text-red-400'}`}>
                {health.models.distilbert.loaded ? '✅ Cargado' : '❌ No disponible'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Comparación DistilBERT vs LR */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* DistilBERT */}
        <div className="bg-gradient-to-br from-purple-900 to-pink-900 rounded-xl p-6 border-2 border-purple-600">
          <div className="text-center mb-6">
            <div className="text-6xl mb-3">🤖</div>
            <h3 className="text-2xl font-bold text-white mb-2">DistilBERT</h3>
            <p className="text-gray-300 text-sm">Transformer Fine-tuned (Producción)</p>
          </div>

          <div className="space-y-4">
            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Test Accuracy</span>
                <span className="text-green-400 font-bold text-xl">{distilbertMetrics.test_accuracy}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-full rounded-full" style={{ width: `${distilbertMetrics.test_accuracy}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">F1-Score</span>
                <span className="text-blue-400 font-bold text-xl">{distilbertMetrics.f1_score}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-blue-500 h-full rounded-full" style={{ width: `${distilbertMetrics.f1_score}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Precision</span>
                <span className="text-purple-400 font-bold text-xl">{distilbertMetrics.precision}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-purple-500 h-full rounded-full" style={{ width: `${distilbertMetrics.precision}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Recall</span>
                <span className="text-pink-400 font-bold text-xl">{distilbertMetrics.recall}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-pink-500 h-full rounded-full" style={{ width: `${distilbertMetrics.recall}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Overfitting</span>
                <span className="text-green-400 font-bold text-xl">{distilbertMetrics.overfitting}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-full rounded-full" style={{ width: `${distilbertMetrics.overfitting}%` }}></div>
              </div>
              <p className="text-xs text-gray-400 mt-1">✅ Excelente ({distilbertMetrics.overfitting}% {'<'} 10%)</p>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Parámetros</span>
                <span className="text-yellow-400 font-bold text-xl">{distilbertMetrics.parameters}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Logistic Regression */}
        <div className="bg-gradient-to-br from-blue-900 to-cyan-900 rounded-xl p-6 border-2 border-blue-600">
          <div className="text-center mb-6">
            <div className="text-6xl mb-3">📊</div>
            <h3 className="text-2xl font-bold text-white mb-2">Logistic Regression</h3>
            <p className="text-gray-300 text-sm">Baseline Model (Comparación)</p>
          </div>

          <div className="space-y-4">
            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Test Accuracy</span>
                <span className="text-orange-400 font-bold text-xl">{logisticMetrics.test_accuracy}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-orange-500 h-full rounded-full" style={{ width: `${logisticMetrics.test_accuracy}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">F1-Score</span>
                <span className="text-yellow-400 font-bold text-xl">{logisticMetrics.f1_score}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-yellow-500 h-full rounded-full" style={{ width: `${logisticMetrics.f1_score}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Precision</span>
                <span className="text-red-400 font-bold text-xl">{logisticMetrics.precision}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-red-500 h-full rounded-full" style={{ width: `${logisticMetrics.precision}%` }}></div>
              </div>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Recall (Toxic)</span>
                <span className="text-green-400 font-bold text-xl">{logisticMetrics.recall_toxic}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-full rounded-full" style={{ width: `${logisticMetrics.recall_toxic}%` }}></div>
              </div>
              <p className="text-xs text-gray-400 mt-1">⚠️ Alto recall pero baja precision</p>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-300">Overfitting</span>
                <span className="text-red-400 font-bold text-xl">{logisticMetrics.overfitting}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div className="bg-red-500 h-full rounded-full" style={{ width: `${logisticMetrics.overfitting}%` }}></div>
              </div>
              <p className="text-xs text-gray-400 mt-1">⚠️ Alto overfitting ({logisticMetrics.overfitting}% {'>'} 10%)</p>
            </div>

            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Threshold</span>
                <span className="text-cyan-400 font-bold text-xl">0.3</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabla Comparativa */}
      <div className="bg-gray-800 rounded-xl p-6 overflow-x-auto">
        <h2 className="text-2xl font-bold text-white mb-6">📈 Tabla Comparativa</h2>
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="pb-3 text-gray-400">Métrica</th>
              <th className="pb-3 text-center text-purple-400">🤖 DistilBERT</th>
              <th className="pb-3 text-center text-blue-400">📊 Logistic Regression</th>
              <th className="pb-3 text-center text-gray-400">Ganador</th>
            </tr>
          </thead>
          <tbody className="text-white">
            <tr className="border-b border-gray-700">
              <td className="py-3">Accuracy</td>
              <td className="text-center font-bold text-green-400">{distilbertMetrics.test_accuracy}%</td>
              <td className="text-center">{logisticMetrics.test_accuracy}%</td>
              <td className="text-center">⭐ DistilBERT</td>
            </tr>
            <tr className="border-b border-gray-700">
              <td className="py-3">F1-Score</td>
              <td className="text-center font-bold text-green-400">{distilbertMetrics.f1_score}%</td>
              <td className="text-center">{logisticMetrics.f1_score}%</td>
              <td className="text-center">⭐ DistilBERT</td>
            </tr>
            <tr className="border-b border-gray-700">
              <td className="py-3">Precision</td>
              <td className="text-center font-bold text-green-400">{distilbertMetrics.precision}%</td>
              <td className="text-center">{logisticMetrics.precision}%</td>
              <td className="text-center">⭐ DistilBERT</td>
            </tr>
            <tr className="border-b border-gray-700">
              <td className="py-3">Overfitting</td>
              <td className="text-center font-bold text-green-400">{distilbertMetrics.overfitting}%</td>
              <td className="text-center text-red-400">{logisticMetrics.overfitting}%</td>
              <td className="text-center">⭐ DistilBERT</td>
            </tr>
            <tr>
              <td className="py-3">Velocidad</td>
              <td className="text-center">~200ms</td>
              <td className="text-center font-bold text-green-400">~20ms</td>
              <td className="text-center">⭐ Logistic Regression</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Recomendación Final */}
      <div className="bg-gradient-to-r from-green-900 to-emerald-900 rounded-xl p-6 border-2 border-green-600">
        <h2 className="text-2xl font-bold text-white mb-4">✅ Recomendación</h2>
        <div className="space-y-3 text-gray-200">
          <p className="flex items-start gap-2">
            <span className="text-green-400 text-xl">•</span>
            <span><strong>DistilBERT</strong> es claramente superior en accuracy ({distilbertMetrics.test_accuracy}% vs {logisticMetrics.test_accuracy}%), F1-score y overfitting mínimo ({distilbertMetrics.overfitting}%).</span>
          </p>
          <p className="flex items-start gap-2">
            <span className="text-green-400 text-xl">•</span>
            <span>Para <strong>producción</strong>, DistilBERT ofrece el mejor balance entre precisión y generalización.</span>
          </p>
          <p className="flex items-start gap-2">
            <span className="text-yellow-400 text-xl">•</span>
            <span>Logistic Regression puede ser útil para <strong>comparaciones rápidas</strong> o cuando la velocidad es crítica (~10x más rápido).</span>
          </p>
        </div>
      </div>
    </div>
  )
}

export default ModelMetrics