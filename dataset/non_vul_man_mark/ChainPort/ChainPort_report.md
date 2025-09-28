# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokensFreezed1, TokensUnfreezed2
- **rel_chain**: CreatedPendingWithdrawal, WithdrawalApproved, WithdrawalRejected
- **det_chain**: TokensUnfreezed1, TokensFreezed2
### src_chain: Ethereum
- **事件**: TokensFreezed1
  - 函数: freezeToken
  - 关键操作: require(result, "Transfer did not go through.")
- **事件**: TokensUnfreezed2
  - 函数: releaseTokens
  - 关键操作: require(isTokenHavingPendingWithdrawal[token] == false), require(isSignatureUsed[signature] == false), isSignatureUsed[signature] = true, require(isMessageValid == true, "Error: Signature is not valid."), require(result, "Transfer did not go through.")
### rel_chain: RelayChain
- **事件**: CreatedPendingWithdrawal
  - 函数: releaseTokens
  - 关键操作: require(isTokenHavingPendingWithdrawal[token] == false), require(isSignatureUsed[signature] == false), isSignatureUsed[signature] = true, require(isMessageValid == true, "Error: Signature is not valid.")
- **事件**: WithdrawalApproved
  - 函数: approveWithdrawalAndTransferFunds
  - 关键操作: require(isTokenHavingPendingWithdrawal[token] == true), require(result, "Transfer did not go through.")
- **事件**: WithdrawalRejected
  - 函数: rejectWithdrawal
  - 关键操作: require(isTokenHavingPendingWithdrawal[token] == true)
### det_chain: Ethereum
- **事件**: TokensUnfreezed1
  - 函数: releaseTokens
  - 关键操作: require(isTokenHavingPendingWithdrawal[token] == false), require(isSignatureUsed[signature] == false), isSignatureUsed[signature] = true, require(isMessageValid == true, "Error: Signature is not valid."), require(result, "Transfer did not go through.")
- **事件**: TokensFreezed2
  - 函数: freezeToken
  - 关键操作: require(result, "Transfer did not go through.")
---
