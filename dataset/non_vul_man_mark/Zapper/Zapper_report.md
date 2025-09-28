# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: ZapIn
- **rel_chain**: _fillQuote, _subtractGoodwill
- **det_chain**: ZapOut
### src_chain: Ethereum
- **事件**: ZapIn
  - 函数: ZapIn
  - 关键操作: require(msg.value > 0, "No eth sent"), uint256 toInvest = _pullTokens(fromToken, amountIn, affiliate, true);
### rel_chain: Polygon
- **事件**: _fillQuote
  - 函数: _fillQuote
  - 关键操作: require(approvedTargets[swapTarget], "Target not Authorized");, (bool success, ) = swapTarget.call{ value: valueToSend }(swapCallData); require(success, "Error Swapping Tokens");
- **事件**: _subtractGoodwill
  - 函数: _subtractGoodwill
  - 关键操作: totalGoodwillPortion = (amount * goodwill) / 10000;, affiliateBalance[affiliate][token] += affiliatePortion;
### det_chain: Polygon
- **事件**: ZapOut
  - 函数: ZapOut
  - 关键操作: uint256 tokensRec = _pullTokens(fromToken, amountIn);, IERC20(toToken).safeTransfer(msg.sender, tokensRec);
---
