# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: SetCallableAddress1, TransferToken2
- **det_chain**: Swapped1, FeeWalletUpdated2, WETHUpdated3, WETHDfynUpdated4, DODOApproveUpdated5, ArkenApproveUpdated6, UniswapV3FactoryUpdated7
### src_chain: ethereum
- **事件**: SetCallableAddress1
  - 函数: initializeCallableAddress
  - 关键操作: require(_CALLABLE_ADDRESS_ == address(0), 'ArkenApprove: callable address initialized')
- **事件**: TransferToken2
  - 函数: transferToken
  - 关键操作: if (amount > 0), token.safeTransferFrom(from, to, amount)
### rel_chain: none
- 无事件
### det_chain: ethereum
- **事件**: Swapped1
  - 函数: trade
  - 关键操作: require(desc.amountIn > 0, 'Amount-in needs to be more than zero'), require(desc.amountOutMin > 0, 'Amount-out minimum needs to be more than zero'), if (_ETH_ == desc.srcToken), require(desc.isRouterSource, 'Source token Ether requires isRouterSource=true'), if (returnAmount > 0), emit Swapped(desc.srcToken, desc.dstToken, desc.amountIn, receivedAmt)
- **事件**: FeeWalletUpdated2
  - 函数: updateFeeWallet
  - 关键操作: require(_feeWallet != address(0), 'fee wallet zero address'), _FEE_WALLET_ADDR_ = _feeWallet, emit FeeWalletUpdated(_FEE_WALLET_ADDR_)
- **事件**: WETHUpdated3
  - 函数: updateWETH
  - 关键操作: require(_weth != address(0), 'WETH zero address'), _WETH_ = _weth, emit WETHUpdated(_WETH_)
- **事件**: WETHDfynUpdated4
  - 函数: updateWETHDfyn
  - 关键操作: require(_weth_dfyn != address(0), 'WETH dfyn zero address'), _WETH_DFYN_ = _weth_dfyn, emit WETHDfynUpdated(_WETH_DFYN_)
- **事件**: DODOApproveUpdated5
  - 函数: updateDODOApproveAddress
  - 关键操作: require(_dodoApproveAddress != address(0), 'dodo approve zero address'), _DODO_APPROVE_ADDR_ = _dodoApproveAddress, emit DODOApproveUpdated(_DODO_APPROVE_ADDR_)
- **事件**: ArkenApproveUpdated6
  - 函数: updateArkenApprove
  - 关键操作: require(_arkenApprove != address(0), 'arken approve zero address'), _ARKEN_APPROVE_ = _arkenApprove, emit ArkenApproveUpdated(_ARKEN_APPROVE_)
- **事件**: UniswapV3FactoryUpdated7
  - 函数: updateUniswapV3Factory
  - 关键操作: require(_uv3Factory != address(0), 'UniswapV3 Factory zero address'), _UNISWAP_V3_FACTORY_ = _uv3Factory, emit UniswapV3FactoryUpdated(_UNISWAP_V3_FACTORY_)
---
