<transition name="modal" id="modal-template">
	<div class="modal-mask">
		<div>
			<span class="close" @click="$emit('close')">×</span>
		</div>
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="modal-header">
					<slot name="header">
						[[ product ]]
					</slot>
				</div>

				<div class="modal-body">
					<slot name="body">
						default body
					</slot>
				</div>

				<div class="modal-footer">
					<slot name="footer">
						default footer
					</slot>
				</div>
			</div>
		</div>
	</div>
</transition>