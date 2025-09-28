# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: RequestSent1
- **det_chain**: CrossChainProcessed1
### src_chain: source_chain
- **事件**: RequestSent1
  - 函数: crossChainWithSwap
  - 关键操作: IERC20(_params.srcInputToken).transferFrom(msg.sender, address(this), _params.srcInputAmount), accrueFixedCryptoFee(_params.integrator, _info), accrueTokenFees(_params.integrator, _info, _params.srcInputAmount, 0, _params.srcInputToken), SmartApprove.smartApprove(_params.srcInputToken, _amountIn, _params.router), ITestDEX(_params.router).swap(_params.srcInputToken, _amountIn, _params.dstOutputToken)
### rel_chain: 
- 无事件
### det_chain: destination_chain
- **事件**: CrossChainProcessed1
  - 函数: 
---
