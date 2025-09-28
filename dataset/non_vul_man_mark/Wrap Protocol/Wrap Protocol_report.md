# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: ERC20WrapAsked1, ERC721WrapAsked1
- **rel_chain**: ExecutionSuccess, ExecutionFailure
- **det_chain**: onERC721Received1, onERC20TransferReceived1
### src_chain: Ethereum
- **事件**: ERC20WrapAsked1
  - 函数: wrapERC20
  - 关键操作: require(amount > 0, "WRAP: INVALID_AMOUNT"), _erc20SafeTransferFrom(token, msg.sender, address(this), amount)
- **事件**: ERC721WrapAsked1
  - 函数: wrapERC721
  - 关键操作: _erc721SafeTransferFrom(token, msg.sender, address(this), tokenId)
### rel_chain: RelayChain
- **事件**: ExecutionSuccess
  - 函数: execTransaction
  - 关键操作: require(tezosOperations[tezosOperation] == false, 'WRAP: TRANSACTION_ALREADY_PROCESSED'), tezosOperations[tezosOperation] = true, _checkSignatures(txHash, signatures), success = _execute(to, value, data, gasleft())
- **事件**: ExecutionFailure
  - 函数: execTransaction
  - 关键操作: require(tezosOperations[tezosOperation] == false, 'WRAP: TRANSACTION_ALREADY_PROCESSED'), tezosOperations[tezosOperation] = true, _checkSignatures(txHash, signatures), success = _execute(to, value, data, gasleft())
### det_chain: Tezos
- **事件**: onERC721Received1
  - 函数: onERC721Received
- **事件**: onERC20TransferReceived1
  - 函数: _erc20SafeTransferFrom
  - 关键操作: (bool success, bytes memory data) = token.call(abi.encodeWithSelector(ERC20_TRANSFER_SELECTOR, from, to, value)), require(success && (data.length == 0 || abi.decode(data, (bool))), 'WRAP: ERC20_TRANSFER_FAILED')
---
