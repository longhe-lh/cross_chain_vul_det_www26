# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposited1, TokenWithdrew2
- **rel_chain**: ValidatorAdded, ValidatorRemoved, ThresholdUpdated
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Mainchain
- **事件**: TokenDeposited1
  - 函数: depositEthFor
  - 关键操作: WETH(_weth).deposit.value(msg.value)(), _createDepositEntry
  - 函数: depositERC20For
  - 关键操作: IERC20(_token).transferFrom, _createDepositEntry
  - 函数: depositERC721For
  - 关键操作: IERC721(_token).transferFrom, _createDepositEntry
- **事件**: TokenWithdrew2
  - 函数: withdrawERC20For
  - 关键操作: IERC20Mintable(_token).mint, IERC20(_token).transfer
  - 函数: withdrawERC721For
  - 关键操作: IERC721Mintable(_token).mint
### rel_chain: RelayChain
- **事件**: ValidatorAdded
  - 函数: addValidators
  - 关键操作: _addValidator, validatorCount++
- **事件**: ValidatorRemoved
  - 函数: removeValidator
  - 关键操作: _removeValidator, validatorCount--
- **事件**: ThresholdUpdated
  - 函数: updateQuorum
  - 关键操作: _updateQuorum
### det_chain: Sidechain
- **事件**: TokenWithdraw1
  - 函数: claim
  - 关键操作: claimed[account] = true, IERC20(token).transfer
- **事件**: TokenMint2
  - 函数: mint
  - 关键操作: totalSupply = totalSupply.add, balanceOf[_to] = balanceOf[_to].add, emit Transfer
---
