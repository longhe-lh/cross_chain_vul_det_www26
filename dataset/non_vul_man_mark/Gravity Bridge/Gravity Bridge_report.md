# 跨链桥合约分析报告
## 跨链桥: Gravity
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SendToCosmosEvent1, TransactionBatchExecutedEvent1, LogicCallEvent1, ERC20DeployedEvent1
- **rel_chain**: ValsetUpdatedEvent
- **det_chain**: SendToCosmosEvent1, TransactionBatchExecutedEvent1, LogicCallEvent1, ERC20DeployedEvent1
### src_chain: Ethereum
- **事件**: SendToCosmosEvent1
  - 函数: sendToCosmos
  - 关键操作: IERC20(_tokenContract).safeTransferFrom(msg.sender, address(this), _amount), require(ourEndingBalance <= ourStartingBalance, "InvalidSendToCosmos()");
- **事件**: TransactionBatchExecutedEvent1
  - 函数: submitBatch
  - 关键操作: IERC20(_tokenContract).safeTransfer(_destinations[i], _amounts[i]), IERC20(_tokenContract).safeTransfer(msg.sender, totalFee)
- **事件**: LogicCallEvent1
  - 函数: submitLogicCall
  - 关键操作: IERC20(_args.transferTokenContracts[i]).safeTransfer(_args.logicContractAddress, _args.transferAmounts[i]), Address.functionCall(_args.logicContractAddress, _args.payload), IERC20(_args.feeTokenContracts[i]).safeTransfer(msg.sender, _args.feeAmounts[i])
- **事件**: ERC20DeployedEvent1
  - 函数: deployERC20
  - 关键操作: new CosmosERC20(address(this), _name, _symbol, _decimals)
### rel_chain: Cosmos
- **事件**: ValsetUpdatedEvent
  - 函数: updateValset
  - 关键操作: require(_newValset.valsetNonce <= _currentValset.valsetNonce, "InvalidValsetNonce()"), require(_newValset.valsetNonce > _currentValset.valsetNonce + 1000000, "InvalidValsetNonce()"), require(_newValset.validators.length != _newValset.powers.length || _newValset.validators.length == 0, "MalformedNewValidatorSet()"), require(_currentValset.validators.length != _currentValset.powers.length || _currentValset.validators.length != _sigs.length, "MalformedCurrentValidatorSet()"), require(cumulativePower <= constant_powerThreshold, "InsufficientPower()"), require(makeCheckpoint(_currentValset, state_gravityId) != state_lastValsetCheckpoint, "IncorrectCheckpoint()"), require(block.number >= _batchTimeout, "BatchTimedOut()")
### det_chain: Ethereum
- **事件**: SendToCosmosEvent1
  - 函数: sendToCosmos
  - 关键操作: IERC20(_tokenContract).safeTransferFrom(msg.sender, address(this), _amount), require(ourEndingBalance <= ourStartingBalance, "InvalidSendToCosmos()");
- **事件**: TransactionBatchExecutedEvent1
  - 函数: submitBatch
  - 关键操作: IERC20(_tokenContract).safeTransfer(_destinations[i], _amounts[i]), IERC20(_tokenContract).safeTransfer(msg.sender, totalFee)
- **事件**: LogicCallEvent1
  - 函数: submitLogicCall
  - 关键操作: IERC20(_args.transferTokenContracts[i]).safeTransfer(_args.logicContractAddress, _args.transferAmounts[i]), Address.functionCall(_args.logicContractAddress, _args.payload), IERC20(_args.feeTokenContracts[i]).safeTransfer(msg.sender, _args.feeAmounts[i])
- **事件**: ERC20DeployedEvent1
  - 函数: deployERC20
  - 关键操作: new CosmosERC20(address(this), _name, _symbol, _decimals)
---
