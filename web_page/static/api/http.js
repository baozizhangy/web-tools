// api.js

export async function callApi(endpoint, params = {}, method = 'POST') {
    try {
        // 构造 fetch 配置对象
        const config = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
            },
        };

        // 针对不同请求方法调整配置
        if (method.toUpperCase() === 'GET') {
            // 将参数拼接到 URL 上（GET 请求）
            const urlParams = new URLSearchParams(params).toString();
            endpoint = urlParams ? `${endpoint}?${urlParams}` : endpoint;
        } else {
            // 其他请求方法默认使用 body
            config.body = JSON.stringify(params);
        }

        // 发起请求
        const response = await fetch(endpoint, config);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 解析 JSON 数据
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}
