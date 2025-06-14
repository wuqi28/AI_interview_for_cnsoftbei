// 生成题目
export async function generateQuestions(filters) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/interview/generate_questions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filters),
    });
    const result = await response.json();
    const text = result.data.outputs.text
    const questions = []
    text.knowledgePoints.forEach((kp) => {
        kp.questions.forEach((q) => {
        questions.push(q)
      })
  })
  return questions
  } catch (error) {
    console.error("Backend API Error:", error);
    throw new Error(`生成题目失败: ${error.message}`);
  }
}