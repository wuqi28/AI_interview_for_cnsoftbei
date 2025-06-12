// import * as tf from '@tensorflow/tfjs';
import Human from '@vladmandic/human';


const humanConfig = {
  modelBasePath: '/models', // 注意你需要把模型文件放到 public/models 下
  cacheSensitivity: 0,
  face: {
    enabled: true,
    detector: { enabled: true },
    mesh: { enabled: true },
    iris: { enabled: true},
    emotion: { enabled: true }
  },
};

const human = new Human(humanConfig);
export default human;
